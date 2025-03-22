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

# Create an email object
email = Email(
    sender="john.doe@example.com",
    subject="Adjustment Request for Loan #12345",
    date="2025-03-22",
    body="Hello, I need to adjust the principal amount of my loan #12345. The adjustment should be effective from 2025-04-01. Reason: Incorrect disbursement. Please approve.",
    attachments=[],
)

# Process the email
response = email_processor.process_email(email)
print(response)
