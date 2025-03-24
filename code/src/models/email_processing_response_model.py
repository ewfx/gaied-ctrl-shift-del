from typing import List, Dict, Any

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
    def __init__(self, responses: List[ServiceRequestResponse]):
        self.responses = responses

    def __repr__(self) -> str:
        return f"EmailProcessingResponse(\n  responses: [\n    " + ",\n    ".join(repr(response) for response in self.responses) + "\n  ]\n)"

    def flatten(self) -> List[ServiceRequestResponse]:
        """
        Flatten the responses by creating separate entries for each subtype.
        """
        flattened_responses = []
        for response in self.responses:
            if response.sub_request_type:
                flattened_responses.append(ServiceRequestResponse(
                    response.request_type,
                    response.sub_request_type,
                    response.fields,
                    response.confidence_score
                ))
            else:
                flattened_responses.append(response)
        return flattened_responses