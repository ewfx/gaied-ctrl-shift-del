from typing import List, Dict, Any, Optional

class ServiceRequestResponse:
    def __init__(self, request_type: str, sub_request_type: str, fields: Dict[str, Any], confidence_score: float):
        self.request_type = request_type
        self.sub_request_type = sub_request_type
        self.fields = fields
        self.confidence_score = confidence_score

    def __repr__(self) -> str:
        fields_str = ", ".join(f"{key}: {value}" for key, value in self.fields.items())
        return (
            f"ServiceRequestResponse(\n"
            f"  request_type: '{self.request_type}',\n"
            f"  sub_request_type: '{self.sub_request_type}',\n"
            f"  fields: {{ {fields_str} }},\n"
            f"  confidence_score: {self.confidence_score:.2f}\n"
            f")\n"
        )


class EmailProcessingResponse:
    def __init__(
        self,
        status: str,  # "processed", "skipped", or "failed"
        responses: Optional[List[ServiceRequestResponse]] = None,
        reasonForNotProcessing: Optional[str] = None  # Only used if status is "skipped" or "failed"
    ):
        self.status = status
        self.responses = responses or []
        self.reasonForNotProcessing = reasonForNotProcessing if status in ["skipped", "failed"] else None

    def __repr__(self) -> str:
        response_str = ",\n    ".join(repr(response) for response in self.responses) if self.responses else "[]"
        reason_str = f"  reasonForNotProcessing: '{self.reasonForNotProcessing}',\n" if self.reasonForNotProcessing else ""
        return (
            f"EmailProcessingResponse(\n"
            f"  status: '{self.status}',\n"
            f"{reason_str}"
            f"  responses: [\n    {response_str}\n  ]\n"
            f")\n"
        )
