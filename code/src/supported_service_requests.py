# List to store service request definitions
from models.service_request_model import ServiceRequest


supported_service_requests = {
    "Adjustment": ServiceRequest(
        request_type="Adjustment",
        description="Request to adjust loan parameters such as fees or principal.",
        dynamic_fields={
            "Adjustment Type": "Required",  # Reallocation Fees / Amendment Fees / Reallocation Principal
            "Amount": "Required",
            "Effective Date": "Required",
            "Reason for Adjustment": "Required",
            "Approving Authority": "Required",
        },
    ),
    "AU Transfer": ServiceRequest(
        request_type="AU Transfer",
        description="Transfer funds between internal bank accounts.",
        dynamic_fields={
            "From Account ID": "Required",
            "To Account ID": "Required",
            "Transfer Amount": "Required",
            "Transfer Date": "Required",
            "Reference ID": "Required",
            "Remarks": "Optional",
        },
    ),
    "Closing Notice": ServiceRequest(
        request_type="Closing Notice",
        description="Finalize a loan and handle outstanding balances.",
        dynamic_fields={
            "Closing Type": "Required",  # Cashless Roll / Reallocation Principal
            "Final Payment Amount": "Required",
            "Closing Date": "Required",
            "Remaining Balance": "Optional",
            "Settlement Instructions": "Required",
        },
    ),
    "Commitment Change": ServiceRequest(
        request_type="Commitment Change",
        description="Modify the committed loan amount.",
        dynamic_fields={
            "Change Type": "Required",  # Increase / Decrease
            "New Commitment Amount": "Required",
            "Effective Date": "Required",
            "Reason for Change": "Required",
            "Approval Details": "Required",
        },
    ),
    "Fee Payment": ServiceRequest(
        request_type="Fee Payment",
        description="Process a payment for loan-related fees.",
        dynamic_fields={
            "Fee Type": "Required",  # Ongoing Fee / Letter of Credit Fee
            "Fee Amount": "Required",
            "Payment Date": "Required",
            "Payment Method": "Required",
            "Invoice Reference": "Optional",
        },
    ),
    "Money Movement - Inbound": ServiceRequest(
        request_type="Money Movement - Inbound",
        description="Receive payments from borrowers.",
        dynamic_fields={
            "Payment Type": "Required",  # Principal / Interest / Principal + Interest / Principal + Interest + Fee
            "Amount Paid": "Required",
            "Payment Date": "Required",
            "Payer Details": "Required",
            "Payment Mode": "Required",
            "Reference Number": "Optional",
        },
    ),
    "Money Movement - Outbound": ServiceRequest(
        request_type="Money Movement - Outbound",
        description="Bank disburses payments such as loan disbursement.",
        dynamic_fields={
            "Payment Type": "Required",  # Timebound / Foreign Currency
            "Amount": "Required",
            "Currency": "Required",
            "Recipient Details": "Required",
            "Payment Date": "Required",
            "Payment Mode": "Required",
            "Exchange Rate": "Optional",
        },
    ),
}

# Display all request types
if __name__ == "__main__":
    for request_type in supported_service_requests:
        supported_service_requests[request_type].display_definition()
        print("\n" + "-" * 50 + "\n")
