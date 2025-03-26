import logging
import json
import re
from typing import Dict, List, Tuple, Any
from email_preprocessor import EmailPreprocessor
from llm_service import HuggingFaceLLM, HuggingFaceModel
from models.email_model import Email
from models.email_processing_response_model import (
    EmailProcessingResponse,
    ServiceRequestResponse,
)
from models.service_request_model import ServiceRequest


class EmailProcessor:
    def __init__(
        self,
        llm_service: HuggingFaceLLM,
        service_request_definitions: Dict[str, ServiceRequest],
        confidence_threshold: float = 0.6,
    ):
        """
        Initialize the Email Processor.
        """
        self.llm_service = llm_service
        self.service_request_definitions = service_request_definitions
        self.confidence_threshold = confidence_threshold
        self.preprocessing_service = EmailPreprocessor()
        logging.basicConfig(level=logging.INFO)

    def process_email(self, email: Email) -> EmailProcessingResponse:
        """
        Process an email by first converting it into a structured classification input,
        then classifying it into service request types and extracting relevant fields.
        """
        classification_input = self.preprocessing_service.preprocess_email(email)
        service_requests = self._classify_email(
            classification_input.subject,
            classification_input.body,
            classification_input.attachments,
        )

        # **Check for API Failure Case**
        if service_requests and service_requests[0][0] == "API Failure":
            return EmailProcessingResponse(
                status="failed", reasonForNotProcessing="API failure during classification."
            )

        responses = []
        for request_type, sub_service_requests, confidence_score in service_requests:
            service_request = self.service_request_definitions.get(request_type)
            if not service_request:
                responses.append(
                    ServiceRequestResponse("Unknown", "", {}, confidence_score)
                )
                continue

            extracted_fields = self._extract_fields(
                classification_input.subject,
                classification_input.body,
                classification_input.attachments,
                service_request,
                sub_service_requests,
                confidence_score,
            )
            for sub_request_type, sub_request_score, fields in extracted_fields:
                responses.append(
                    ServiceRequestResponse(
                        request_type, sub_request_type, fields, sub_request_score
                    )
                )
         # **Return "Unclassified" if no valid responses exist**
        if not responses:
            return EmailProcessingResponse(
                status="unclassified", reasonForNotProcessing="No valid classification found."
            )   
        return EmailProcessingResponse(responses=responses,status="processed")

    def _classify_email(
        self, email_subject: str, email_body: str, attachments: List[str]
    ) -> List[Tuple[str, List[Tuple[str, float]], float]]:
        """
        Classifies an email into one or more service request types using zero-shot classification.
        """
        full_text = f"Subject: {email_subject}\nBody: {email_body}"

        labels = [f"{key} Request" for key in self.service_request_definitions.keys()]
        classification_result = self.llm_service.zero_shot_classify(
            HuggingFaceModel.MORITZ_LAURER_DEBERT, full_text, labels, True
        )

        # **Handle API Failure Case**
        if "error" in classification_result:
            logging.error(f"LLM API failure: {classification_result['error']}")
            return [("API Failure", [], 0.0)]  # Mark as API failure explicitly

        # **Handle Unclassified Cases**
        if "labels" not in classification_result or not classification_result["labels"]:
            return [("Unclassified", [], 0.0)]

        service_requests = []
        for label, score in zip(
            classification_result["labels"], classification_result["scores"]
        ):
            if score < self.confidence_threshold:
                continue
            best_request_key = label.rsplit(" Request", 1)[0]

            sub_service_requests = []
            if best_request_key in self.service_request_definitions:
                sub_labels = [
                    f"{key} Request"
                    for key in self.service_request_definitions[
                        best_request_key
                    ].sub_service_requests.keys()
                ]
                if sub_labels:
                    sub_classification_result = self.llm_service.zero_shot_classify(
                        HuggingFaceModel.MORITZ_LAURER_DEBERT,
                        full_text,
                        sub_labels,
                        True,
                    )

                    # **Handle Sub-Classification API Failure**
                    if "error" in sub_classification_result:
                        logging.error(
                            f"LLM API failure in sub-classification: {sub_classification_result['error']}"
                        )
                        return [
                            ("API Failure", [], 0.0)
                        ]  # Ensure consistent failure handling

                    if (
                        "labels" in sub_classification_result
                        and sub_classification_result["labels"]
                    ):
                        for sub_label, sub_score in zip(
                            sub_classification_result["labels"],
                            sub_classification_result["scores"],
                        ):
                            if sub_score >= self.confidence_threshold:
                                sub_best_match_label = sub_label.rsplit(" Request", 1)[
                                    0
                                ]
                                sub_service_requests.append(
                                    (sub_best_match_label, sub_score)
                                )

            service_requests.append((best_request_key, sub_service_requests, score))

        return service_requests

    def _extract_fields(
        self,
        email_subject: str,
        email_body: str,
        attachments: str,
        service_request: ServiceRequest,
        sub_service_requests: List[Tuple[str, float]],
        confidence_score: float,
    ) -> List[Tuple[str, float, Dict[str, Any]]]:
        extracted_fields_list = []

        for sub_request_type, sub_request_score in sub_service_requests or [
            (None, confidence_score)
        ]:
            fields_to_extract = service_request.get_all_fields()
            if sub_request_type:
                sub_fields = service_request.get_sub_service_fields(sub_request_type)
                fields_to_extract.update(sub_fields)

            if not fields_to_extract:
                extracted_fields_list.append((sub_request_type, sub_request_score, {}))
                continue

            prompt = f"""
            Extract the following fields from this customer email:
            {', '.join(fields_to_extract)}
            
            Subject: {email_subject}
            
            Body:
            {email_body}
            
            Attachments:
            {attachments}
            
            Return only a valid JSON object with no extra text.
            """

            response = self.llm_service.generate_response(
                HuggingFaceModel.MISTRAL_7B_INSTRUCT, prompt, max_length=200
            )

            match = re.search(r"\{.*\}", response, re.DOTALL)
            if not match:
                logging.error("No valid JSON found in LLM response.")
                extracted_fields = {
                    field: "Not Provided" for field in fields_to_extract
                }
            else:
                try:
                    extracted_data = json.loads(match.group(0))
                    extracted_fields = {
                        field: extracted_data.get(field, "Not Provided")
                        for field in fields_to_extract
                    }
                except json.JSONDecodeError as e:
                    logging.error(f"Error parsing extracted fields: {e}")
                    extracted_fields = {
                        field: "Not Provided" for field in fields_to_extract
                    }

            extracted_fields_list.append(
                (sub_request_type, sub_request_score, extracted_fields)
            )

        return extracted_fields_list
