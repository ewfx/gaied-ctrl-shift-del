# List to store service request definitions
from models.service_request_model import ServiceRequest


supported_service_requests = {
    "Adjustment": ServiceRequest(
        request_type="Adjustment",
        description="Request to adjust financial amounts related to a loan.",
        dynamic_fields={
            "Adjustment Amount": "Required",  # Amount to be adjusted
            "Adjustment Reason": "Required",  # Justification for the adjustment
            "Effective Date": "Required",  # Date when adjustment takes effect
        },
    ),
    "Enquiry": ServiceRequest(
        request_type="Enquiry",
        description="Request to provide information ,clarification or explanation related to accounts,loans and interest rates",
        dynamic_fields={
            "Enquiry Reason": "Required",
        },
        sub_service_requests={
            "Balance Enquiry": ServiceRequest(
                request_type="Balance Enquiry",
                description="Request to provide information about the account balance",
                dynamic_fields={
                    "Account Type": "Required",  # Type of fee being reallocated
                },
            ),
            "Loan Information":ServiceRequest(
                request_type="Loan Information",
                description="Request to provide information about type of loan provided",
                dynamic_fields={
                    "Loan Type": "Required",  # Type of fee being reallocated
                    "Planned Date": "Required",
                },
            ),
        }
    ),
    "AU Transfer": ServiceRequest(
        request_type="AU Transfer",
        description="Request to transfer an asset unit.",
        dynamic_fields={
            "Source AU": "Required",  # Source Asset Unit
            "Target AU": "Required",  # Destination Asset Unit
            "Transfer Amount": "Required",  # Amount being transferred
        },
    ),
    "Closing Notice": ServiceRequest(
        request_type="Closing Notice",
        description="Request related to closing a loan or financial account.",
        dynamic_fields={
            "Closure Date": "Required",  # Date when the loan/account closes
            "Remaining Balance": "Required",  # Outstanding balance at closure
            "Closure Reason": "Required",  # Justification for closing
        },
        sub_service_requests={
            "Reallocation Fees": ServiceRequest(
                request_type="Reallocation Fees",
                description="Request to reallocate fees during closure.",
                dynamic_fields={
                    "Fee Type": "Required",  # Type of fee being reallocated
                    "Reallocation Amount": "Required",  # Amount being moved
                },
            ),
            "Amendment Fees": ServiceRequest(
                request_type="Amendment Fees",
                description="Request to amend fees during closure.",
                dynamic_fields={
                    "Fee Type": "Required",
                    "New Fee Amount": "Required",
                },
            ),
            "Reallocation Principal": ServiceRequest(
                request_type="Reallocation Principal",
                description="Request to reallocate principal during closure.",
                dynamic_fields={
                    "Reallocation Amount": "Required",
                    "Target Account": "Required",  # Where the principal is moved
                },
            ),
        },
    ),
    "Commitment Change": ServiceRequest(
        request_type="Commitment Change",
        description="Request to change commitment terms for a loan.",
        dynamic_fields={
            "Commitment ID": "Required",  # Unique identifier for commitment
            "Change Reason": "Required",  # Justification for the change
        },
        sub_service_requests={
            "Cashless Roll": ServiceRequest(
                request_type="Cashless Roll",
                description="Extend commitment without new cash movement.",
                dynamic_fields={
                    "New Expiry Date": "Required",  # Extension date
                    "Justification": "Required",
                },
            ),
            "Decrease": ServiceRequest(
                request_type="Decrease",
                description="Decrease the commitment amount.",
                dynamic_fields={
                    "New Commitment Amount": "Required",
                    "Effective Date": "Required",
                },
            ),
            "Increase": ServiceRequest(
                request_type="Increase",
                description="Increase the commitment amount.",
                dynamic_fields={
                    "New Commitment Amount": "Required",
                    "Funding Source": "Required",  # Source of additional funds
                },
            ),
        },
    ),
    "Fee Payment": ServiceRequest(
        request_type="Fee Payment",
        description="Request for fee-related payments.",
        dynamic_fields={
            "Payment Date": "Required",
            "Payment Amount": "Required",
            "Payment Method": "Required",  # e.g., Wire Transfer, ACH
        },
        sub_service_requests={
            "Ongoing Fee": ServiceRequest(
                request_type="Ongoing Fee",
                description="Payment of ongoing fees.",
                dynamic_fields={
                    "Fee Period": "Required",  # Monthly, Quarterly, etc.
                    "Due Date": "Required",
                },
            ),
            "Letter of Credit Fee": ServiceRequest(
                request_type="Letter of Credit Fee",
                description="Payment for Letter of Credit fees.",
                dynamic_fields={
                    "LOC Number": "Required",  # Identifier for the Letter of Credit
                    "Fee Due Date": "Required",
                },
            ),
            "Principal": ServiceRequest(
                request_type="Principal",
                description="Payment towards principal amount.",
                dynamic_fields={
                    "Principal Amount": "Required",
                    "Payment Schedule": "Optional",
                },
            ),
            "Interest": ServiceRequest(
                request_type="Interest",
                description="Payment of interest amount.",
                dynamic_fields={
                    "Interest Period": "Required",  # Interest calculation period
                    "Interest Rate": "Required",  # Applied interest rate
                },
            ),
            "Principal + Interest": ServiceRequest(
                request_type="Principal + Interest",
                description="Payment of both principal and interest.",
                dynamic_fields={
                    "Total Payment Amount": "Required",
                    "Breakdown Required": "Optional",  # If separate principal & interest amounts needed
                },
            ),
        },
    ),
    "Money Movement - Inbound": ServiceRequest(
        request_type="Money Movement - Inbound",
        description="Inbound money transfer related to a loan or fee.",
        dynamic_fields={
            "Transfer Date": "Required",
            "Sender Details": "Required",
            "Transfer Amount": "Required",
            "Receiving Account": "Required",
        },
        sub_service_requests={
            "Principal + Interest + Fee": ServiceRequest(
                request_type="Principal + Interest + Fee",
                description="Inbound transfer covering principal, interest, and fees.",
                dynamic_fields={
                    "Principal Component": "Required",
                    "Interest Component": "Required",
                    "Fee Component": "Required",
                },
            ),
        },
    ),
    "Money Movement - Outbound": ServiceRequest(
        request_type="Money Movement - Outbound",
        description="Outbound money transfer related to a loan or fee.",
        dynamic_fields={
            "Transfer Date": "Required",
            "Recipient Details": "Required",
            "Transfer Amount": "Required",
            "Payment Method": "Required",
        },
        sub_service_requests={
            "Timebound": ServiceRequest(
                request_type="Timebound",
                description="Outbound transfer with a time restriction.",
                dynamic_fields={
                    "Execution Date": "Required",
                    "Time Constraint": "Required",
                },
            ),
            "Foreign Currency": ServiceRequest(
                request_type="Foreign Currency",
                description="Outbound transfer in a foreign currency.",
                dynamic_fields={
                    "Currency Type": "Required",  # USD, EUR, INR, etc.
                    "Exchange Rate": "Required",
                },
            ),
        },
    ),
}
