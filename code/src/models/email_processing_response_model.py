from typing import Dict, Any
import json


class EmailProcessingResponse:
    def __init__(
        self,
        request_type: str,
        extracted_fields: Dict[str, Any],
        confidence_score: float,
    ):
        """
        Response model for processed emails.

        :param request_type: Classified request type.
        :param extracted_fields: Dictionary of extracted fields.
        :param confidence_score: Confidence score of the classification.
        """
        self.request_type = request_type
        self.extracted_fields = extracted_fields
        self.confidence_score = confidence_score

    def is_confident(self, threshold: float = 0.6) -> bool:
        """
        Check if the classification confidence is above the threshold.

        :param threshold: Confidence threshold (default is 0.6).
        :return: True if confidence is above threshold, otherwise False.
        """
        return self.confidence_score >= threshold

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert response to a dictionary format.

        :return: Dictionary representation of the response.
        """
        return {
            "request_type": self.request_type,
            "extracted_fields": self.extracted_fields,
            "confidence_score": self.confidence_score,
        }

    def to_json(self) -> str:
        """
        Convert response to JSON format.

        :return: JSON string of the response.
        """
        return json.dumps(self.to_dict(), indent=4)

    def __repr__(self):
        fields_str = json.dumps(
            self.extracted_fields, indent=2
        )  # Pretty-print JSON fields
        return (
            f"EmailProcessingResponse: \n"
            f"  request_type={self.request_type},\n\n"
            f"  confidence_score={self.confidence_score:.2f},\n\n"
            f"  extracted_fields={fields_str}\n\n"
            f")"
        )
