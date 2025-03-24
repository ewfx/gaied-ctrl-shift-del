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

        return EmailProcessingResponse(responses)

    def _classify_email(
        self, email_subject: str, email_body: str, attachments: List[str]
    ) -> List[Tuple[str, List[Tuple[str, float]], float]]:
        """
        Classifies an email into one or more service request types using zero-shot classification.
        """
        # Combine email body and extracted attachment text
        full_text = f"Subject: {email_subject}\nBody: {email_body}"

        labels = [f"{key} Request" for key in self.service_request_definitions.keys()]
        classification_result = self.llm_service.zero_shot_classify(
            HuggingFaceModel.MORITZ_LAURER_DEBERT, full_text, labels, True
        )

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

    def _create_prompt(
        self,
        fields_to_extract: List[str],
        email_subject: str,
        email_body: str,
        service_request: ServiceRequest,
        attachments: str,
    ) -> str:
        """
        Create a prompt for extracting fields from the email subject and body.
        """
        return f"""
        This is a customer email for a {service_request.request_type} request to a bank. Extract the following fields from the email subject and body, considering different possible names and contexts:
        {', '.join(fields_to_extract)}

        Subject: {email_subject}

        Email:
        {email_body}
        
        Attachments: {attachments}

        Return only a valid JSON object with no extra text, headers, or explanations. If a field is missing, use "N/A".
        """

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

        if not sub_service_requests:
            # If there are no sub-service requests, extract fields for the main service request
            fields_to_extract = service_request.get_all_fields()

            if fields_to_extract:
                prompt = self._create_prompt(
                    fields_to_extract,
                    email_subject,
                    email_body,
                    service_request,
                    attachments,
                )

                response = self.llm_service.generate_response(
                    HuggingFaceModel.MISTRAL_7B_INSTRUCT, prompt, max_length=200
                )

                match = re.search(r"\{.*\}", response, re.DOTALL)
                if not match:
                    logging.error("No valid JSON found in LLM response.")
                    extracted_fields_list.append(
                        (
                            None,
                            0.0,
                            {field: "Not Provided" for field in fields_to_extract},
                        )
                    )
                else:
                    json_text = match.group(0)

                    try:
                        extracted_data = json.loads(json_text)
                    except json.JSONDecodeError as e:
                        logging.error(f"Error parsing extracted fields: {e}")
                        extracted_data = {}

                    extracted_fields = {
                        field: (
                            None
                            if extracted_data.get(field) == "N/A"
                            else extracted_data.get(field, "Not Provided")
                        )
                        for field in fields_to_extract
                    }
                    extracted_fields_list.append(
                        (None, confidence_score, extracted_fields)
                    )
        else:
            # If there are sub-service requests, extract fields for each sub-service request
            for sub_request_type, sub_request_score in sub_service_requests:
                fields_to_extract = service_request.get_all_fields()

                if sub_request_type:
                    sub_fields = service_request.get_sub_service_fields(
                        sub_request_type
                    )
                    fields_to_extract.update(sub_fields)

                if not fields_to_extract:
                    extracted_fields_list.append(
                        (sub_request_type, sub_request_score, {})
                    )
                    continue

                prompt = self._create_prompt(
                    fields_to_extract,
                    email_subject,
                    email_body,
                    service_request,
                    attachments,
                )

                response = self.llm_service.generate_response(
                    HuggingFaceModel.MISTRAL_7B_INSTRUCT, prompt, max_length=200
                )

                match = re.search(r"\{.*\}", response, re.DOTALL)
                if not match:
                    logging.error("No valid JSON found in LLM response.")
                    extracted_fields_list.append(
                        (
                            sub_request_type,
                            sub_request_score,
                            {field: "Not Provided" for field in fields_to_extract},
                        )
                    )
                    continue

                json_text = match.group(0)

                try:
                    extracted_data = json.loads(json_text)
                except json.JSONDecodeError as e:
                    logging.error(f"Error parsing extracted fields: {e}")
                    extracted_data = {}

                extracted_fields = {
                    field: (
                        None
                        if extracted_data.get(field) == "N/A"
                        else extracted_data.get(field, "Not Provided")
                    )
                    for field in fields_to_extract
                }
                extracted_fields_list.append(
                    (sub_request_type, sub_request_score, extracted_fields)
                )

        return extracted_fields_list
