import re

from bs4 import BeautifulSoup
from attachment_processor import AttachmentProcessor
from models.email_model import Email
from models.email_classification_input_model import EmailClassificationInput
import email.utils


class EmailPreprocessor:
    """
    Preprocesses emails and converts them into a structured classification input.
    """

    def __init__(self):
        self.attachment_processor = AttachmentProcessor(folder="./artifacts")

    def preprocess_email(self, email: Email) -> EmailClassificationInput:
        """
        Convert an Email object into an EmailClassificationInput object.
        """
        cleaned_subject = self.clean_text(email.subject)
        cleaned_body = self.clean_text(email.body)
        cleaned_sender = self.extract_email_address(email.sender)
        extracted_attachments = []
        for file_name in email.attachments:
            extracted_text = self.attachment_processor.extract_text_from_attachment(
                file_name
            )
            extracted_attachments.append(extracted_text)

        return EmailClassificationInput(
            subject=cleaned_subject,
            body=cleaned_body,
            sender=cleaned_sender,
            date=email.date,
            attachments=extracted_attachments,  # Store extracted text separately
            metadata={},  # Can be used for additional context
        )

    def clean_text(self, text: str) -> str:
        """
        Cleans email text by removing HTML, extra whitespace, and non-printable characters.
        """
        # Remove HTML tags
        text = BeautifulSoup(text, "html.parser").get_text()

        # Normalize spaces and remove special characters except basic punctuation
        text = re.sub(r"[^\w\s,.!?-]", "", text)

        # Remove extra spaces and strip
        return re.sub(r"\s+", " ", text).strip()

    def extract_email_address(self, sender: str) -> str:
        parsed = email.utils.parseaddr(sender)
        return parsed[1]  # Extracts only the email address
