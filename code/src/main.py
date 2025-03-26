import os
from email_service_manager import EmailServiceManager
from email_processor import EmailProcessor
from llm_service import HuggingFaceLLM
from models.email_model import Email
from supported_service_requests import supported_service_requests

# Initialize the LLM client with your Hugging Face API key
api_key = ""
llm = HuggingFaceLLM(api_key)
email_processor = EmailProcessor(
    llm_service=llm,
    service_request_definitions=supported_service_requests,
    confidence_threshold=0.5,
)

# Simulating a PDF attachment (replace with actual file bytes)
with open("./artifacts/Loan_Adjustment_Request.docx", "rb") as file:
    pdf_bytes = file.read()

# # Create an email object with three service requests
# email = Email(
#     sender="john.doe@example.com",
#     subject="Request for Loan #12345",
#     date="2025-03-22",
#     body=(
#         "Hello, I need to adjust the principal amount of my loan #12345. "
#         "The adjustment should be effective from 2025-04-01. Reason: Incorrect disbursement. "
#         "Please approve.\n\n"
#         "Additionally, I would like to make a fee payment for my loan. The fee amount due is $1,250, "
#         "and I would like to process the payment on 2025-04-01. Please confirm the payment.\n\n"
#     ),
#     attachments=[("loan_details.docx", pdf_bytes)]
# )

# # Process the email
# response = email_processor.process_email(email)
# print(response)

# Initialize EmailProcessor

# Initialize EmailServiceManager
email_service_manager = EmailServiceManager(email_processor)

# Sample emails
email1 = Email(
    sender="customer@example.com",
    subject="Loan Adjustment Request",
    date="2025-03-22",
    body=(
        "Hello, I need to adjust the principal amount of my loan #12345. "
        "The adjustment should be effective from 2025-04-01. Reason: Incorrect disbursement. "
        "Please approve.\n\n"
        "Additionally, I would like to make a fee payment for my loan. The fee amount due is $1,250, "
        "and I would like to process the payment on 2025-04-01. Please confirm the payment.\n\n"
    ),
    attachments=['Loan_Adjustment_Request.docx'],
    thread_id="12345",
    sender_role="customer",
)

email2 = Email(
    sender="support@example.com",
    subject="Re: Loan Adjustment Request",
    date="2025-03-23",
    body="Your loan adjustment has been completed.",
    attachments=[],
    thread_id="12345",
    sender_role="support",
)

email3 = Email(
    sender="customer@example.com",
    subject="Re: Loan Adjustment Request",
    date="2025-03-24",
    body="I need to adjust the principal amount of my loan #12345.",  # Duplicate
    attachments=[],
    thread_id="12345",
    sender_role="customer",
)

# Process emails through EmailServiceManager
response1 = email_service_manager.process_email(email1)  # Should process
response2 = email_service_manager.process_email(email2)  # Should skip (support reply)
response3 = email_service_manager.process_email(email3)  # Should skip (duplicate)

print(response1)
print(response2)
print(response3)
