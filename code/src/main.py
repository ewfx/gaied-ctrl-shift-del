import os
from email_processor import EmailProcessor
from llm_service import HuggingFaceLLM
from models.email_model import Email
from supported_service_requests import supported_service_requests

# Initialize the LLM client with your Hugging Face API key
api_key = "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"
llm = HuggingFaceLLM(api_key)
email_processor = EmailProcessor(
    llm, supported_service_requests, confidence_threshold=0.6
)

# Simulating a PDF attachment (replace with actual file bytes)
with open("./artifacts/Loan_Adjustment_Request.docx", "rb") as file:
    pdf_bytes = file.read()

# Create an email object
email = Email(
    sender="john.doe@example.com",
    subject="Adjustment Request for Loan #12345",
    date="2025-03-22",
    body="Hello, I need to adjust the principal amount of my loan #12345. The adjustment should be effective from 2025-04-01. Reason: Incorrect disbursement. Please approve.",
    attachments=[("loan_details.docx", pdf_bytes)]
)
# email = Email(
#     sender="jane.smith@example.com",
#     subject="Fee Payment Request - Interest for Loan #98765",
#     date="2025-03-22",
#     body="Hello,\n\nI would like to make an interest payment for my loan #98765. The interest amount due is $1,250, and I would like to process the payment on 2025-04-01. Please confirm the payment details.\n\nThank you,\nJane Smith",
# )

# Process the email
response = email_processor.process_email(email)
print(response)
