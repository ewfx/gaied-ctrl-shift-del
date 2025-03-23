class ServiceRequest:
    def __init__(
        self, request_type, description, dynamic_fields, sub_service_requests=None
    ):
        self.request_type = (
            request_type  # Type of service request (e.g., Adjustment, Fee Payment)
        )
        self.description = description  # Brief description of the request
        self.dynamic_fields = (
            dynamic_fields  # Dynamic fields that are specific to the request type
        )
        self.sub_service_requests = sub_service_requests or {}  # Sub-service requests

        # Fixed fields that are always required for any service request
        self.fixed_fields = {
            "Loan Account ID": "Required",  # Unique identifier for the loan
            "Request Date": "Required",  # Date when the request was created
        }

    def get_all_fields(self):
        """Returns a dictionary of all required fields (fixed + dynamic)."""
        all_fields = self.fixed_fields.copy()
        all_fields.update(self.dynamic_fields)
        return all_fields

    def get_sub_service_fields(self, sub_request_type):
        """Returns a dictionary of fields for a specific sub-service request type."""
        if sub_request_type in self.sub_service_requests:
            return self.sub_service_requests[sub_request_type].get_all_fields()
        else:
            return self.get_all_fields()

    def display_definition(self):
        """Displays the service request definition."""
        print(f"Service Request Type: {self.request_type}")
        print(f"Description: {self.description}")
        print("\nFixed Fields (Always Required):")
        for key, value in self.fixed_fields.items():
            print(f"  {key}: {value}")
        print("\nDynamic Fields (Specific to Request Type):")
        for key in self.dynamic_fields:
            print(f"  {key}: Required")
        if self.sub_service_requests:
            print("\nSub-Service Requests:")
            for sub_request_type, sub_request in self.sub_service_requests.items():
                print(f"\n  Sub-Service Request Type: {sub_request_type}")
                sub_request.display_definition()
