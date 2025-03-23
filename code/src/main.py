import os
from email_processor import EmailProcessor
from llm_service import HuggingFaceLLM
from models.email_model import Email
from supported_service_requests import supported_service_requests
from docx import Document

# Initialize the LLM client with your Hugging Face API key
api_key = "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"
llm = HuggingFaceLLM(api_key)
email_processor = EmailProcessor(
    llm, supported_service_requests, confidence_threshold=0.6
)

# Function to read emails from DOCX files in artifacts folder
def read_emails_from_artifacts(folder_path: str):
    emails = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".docx"):
            file_path = os.path.join(folder_path, filename)
            doc = Document(file_path)
            text = "\n".join([para.text for para in doc.paragraphs])
            with open(file_path, "rb") as file:
                file_bytes = file.read()
            emails.append(Email(
                sender="unknown@example.com",
                subject=f"Email extracted from {filename}",
                date="2025-03-22",
                body=text,
                attachments=[(filename, file_bytes)]
            ))
    return emails

# Path to artifacts folder
artifacts_folder = "C:\\Users\\venul\\source\\repos\\gaied-ctrl-shift-del\\artifacts"

# Read emails from artifacts folder
emails = read_emails_from_artifacts(artifacts_folder)

# Process each email
for email in emails:
    response = email_processor.process_email(email)
    print(response)
