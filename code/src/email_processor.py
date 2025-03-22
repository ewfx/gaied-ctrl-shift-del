import logging
import json
import re
from typing import Dict, Tuple, Any
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

        :param llm_service: Instance of the Hugging Face LLM service.
        :param service_request_definitions: Mapping of request types to their definitions.
        :param confidence_threshold: Minimum confidence score required to classify an email automatically.
        """
        self.llm_service = llm_service
        self.service_request_definitions = service_request_definitions
        self.confidence_threshold = confidence_threshold
        logging.basicConfig(level=logging.INFO)

    def process_email(self, email: Email) -> EmailProcessingResponse:
        """
        Process an email by classifying it into a service request type and extracting relevant fields.

        :param email: Email object containing sender, subject, date, body, and attachments.
        :return: An EmailProcessingResponse object containing the request type, extracted fields, and confidence score.
        """
        request_type, confidence_score = self._classify_email(email.subject, email.body)

        if confidence_score < self.confidence_threshold:
            logging.warning(
                "Low confidence classification. Marking as 'Needs Manual Review'."
            )
            return EmailProcessingResponse("Needs Manual Review", {}, confidence_score)

        service_request = self.service_request_definitions.get(request_type)
        if not service_request:
            return EmailProcessingResponse("Unknown", {}, confidence_score)

        extracted_fields = self._extract_fields(
            email.subject, email.body, service_request
        )
        return EmailProcessingResponse(request_type, extracted_fields, confidence_score)

    def _classify_email(self, email_subject: str, email_body: str) -> Tuple[str, float]:
        """
        Classifies an email into a service request type using zero-shot classification.

        :param email_subject: The subject line of the email.
        :param email_body: The text content of the email.
        :return: A tuple containing the classified request type and the confidence score.
        """
        labels = list(self.service_request_definitions.keys())

        # Combine subject and body with priority to subject
        classification_text = (
            f"Subject: {email_subject}\nBody: {email_body[:1000]}"  # Limit body length
        )

        classification_result = self.llm_service.zero_shot_classify(
            HuggingFaceModel.BART_LARGE_MNLI, classification_text, labels
        )

        if "labels" not in classification_result or not classification_result["labels"]:
            logging.warning("Classification failed: No labels returned.")
            return "Unclassified", 0.0

        best_match = classification_result["labels"][0]
        confidence_score = classification_result.get("scores", [0])[0]

        return best_match, confidence_score

    def _extract_fields(
        self,
        email_subject: str,
        email_body: str,
        service_request: ServiceRequest,
    ) -> Dict[str, Any]:
        fields_to_extract = service_request.get_all_fields()

        if not fields_to_extract:
            return {}

        prompt = f"""
        Extract the following fields from the email subject and body, considering different possible names and contexts:
        {', '.join(fields_to_extract)}

        Subject: {email_subject}

        Email:
        {email_body[:2000]}  # Limit body size to avoid model truncation

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
