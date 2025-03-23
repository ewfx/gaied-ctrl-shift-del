import logging
import json
import re
from typing import Dict, List, Tuple, Any
from email_preprocessor import EmailPreprocessor
from llm_service import HuggingFaceLLM, HuggingFaceModel
from models.email_model import Email
from models.email_processing_response_model import EmailProcessingResponse
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
        then classifying it into a service request type and sub-request type before extracting relevant fields.
        """
        classification_input = self.preprocessing_service.preprocess_email(email)
        request_type, sub_request_type, confidence_score = self._classify_email(
            classification_input.subject,
            classification_input.body,
            classification_input.attachments,
        )

        if confidence_score < self.confidence_threshold:
            logging.warning(
                "Low confidence classification. Marking as 'Needs Manual Review'."
            )
            return EmailProcessingResponse("Needs Manual Review", {}, confidence_score)

        service_request = self.service_request_definitions.get(request_type)
        if not service_request:
            return EmailProcessingResponse("Unknown", {}, confidence_score)

        extracted_fields = self._extract_fields(
            classification_input.subject,
            classification_input.body,
            classification_input.attachments,
            service_request,
        )
        return EmailProcessingResponse(f"{request_type} - {sub_request_type}", extracted_fields, confidence_score)

    def _classify_email(
        self, email_subject: str, email_body: str, attachments: List[str]
    ) -> Tuple[str, str, float]:
        """
        Classifies an email into a service request type and sub-request type using zero-shot classification.
        """
        full_text = f"Subject: {email_subject}\nBody: {email_body}"

        # Classify main request type
        labels = list(self.service_request_definitions.keys())
        classification_result = self.llm_service.zero_shot_classify(
            HuggingFaceModel.BART_LARGE_MNLI, full_text, labels
        )

        if "labels" not in classification_result or not classification_result["labels"]:
            return "Unclassified", "Unclassified", 0.0

        request_type = classification_result["labels"][0]
        confidence_score = classification_result["scores"][0]

        # Classify sub-request type if applicable
        sub_request_type = "General"
        if request_type in self.service_request_definitions:
            sub_labels = self.service_request_definitions[request_type].sub_requests
            if sub_labels:
                sub_classification_result = self.llm_service.zero_shot_classify(
                    HuggingFaceModel.BART_LARGE_MNLI, full_text, sub_labels
                )
                if "labels" in sub_classification_result and sub_classification_result["labels"]:
                    sub_request_type = sub_classification_result["labels"][0]

        return request_type, sub_request_type, confidence_score

    def _extract_fields(
        self,
        email_subject: str,
        email_body: str,
        attachments: str,
        service_request: ServiceRequest,
    ) -> Dict[str, Any]:
        fields_to_extract = service_request.dynamic_fields

        if not fields_to_extract:
            return {}

        prompt = f"""
        Extract the following fields from the email subject and body, considering different possible names and contexts:
        {', '.join(fields_to_extract.keys())}

        Subject: {email_subject}

        Email:
        {email_body}
        
        Attachments: {attachments}

        Return only a valid JSON object with no extra text, headers, or explanations. If a field is missing, use "N/A".
        """

        response = self.llm_service.generate_response(
            HuggingFaceModel.MISTRAL_7B_INSTRUCT, prompt, max_length=200
        )

        match = re.search(r"\{.*\}", response, re.DOTALL)
        if not match:
            logging.error("No valid JSON found in LLM response.")
            return {field: "Not Provided" for field in fields_to_extract}

        json_text = match.group(0)

        try:
            extracted_data = json.loads(json_text)
        except json.JSONDecodeError as e:
            logging.error(f"Error parsing extracted fields: {e}")
            extracted_data = {}

        return {
            field: (
                None
                if extracted_data.get(field) == "N/A"
                else extracted_data.get(field, "Not Provided")
            )
            for field in fields_to_extract
        }
