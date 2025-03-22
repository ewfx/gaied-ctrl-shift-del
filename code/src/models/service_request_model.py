class ServiceRequest:
    def __init__(self, request_type, description, dynamic_fields):
        self.request_type = (
            request_type  # Type of service request (e.g., Adjustment, Fee Payment)
        )
        self.description = description  # Brief description of the request

        # Fixed fields that are always required for any service request
        self.fixed_fields = {
            "Loan Account ID": "Required",  # Unique identifier for the loan
            "Request Date": "Required",  # Date when the request was created
        }

        # Dynamic fields that are specific to the request type
        self.dynamic_fields = dynamic_fields

    def get_all_fields(self):
        """Returns a dictionary of all required fields (fixed + dynamic)."""
        all_fields = self.fixed_fields.copy()
        all_fields.update(self.dynamic_fields)
        return all_fields

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
