from models.email_model import Email
from email_thread_manager import EmailThreadManager
from email_processor import EmailProcessor
from models.email_processing_response_model import EmailProcessingResponse


class EmailServiceManager:
    def __init__(self, email_processor: EmailProcessor):
        self.email_processor = email_processor
        self.thread_manager = EmailThreadManager()

    def process_email(self, email: Email) -> EmailProcessingResponse:
        """Main method to process emails, handling threads and duplicates."""

        # **Case 2: Support Email - No Need to Process**
        if email.sender_role == "support":
            return EmailProcessingResponse(
                status="skipped", reasonForNotProcessing="Support email. No processing required."
            )

        self.thread_manager.add_email(email)  # Add email to thread

        # Get last unreplied customer email
        last_email, past_customer_emails = (
            self.thread_manager.get_last_unreplied_customer_email(
                email.thread_id or email.sender
            )
        )

        if not last_email:
            return EmailProcessingResponse(
                status="skipped", reasonForNotProcessing="No open customer request."
            )

        # **Case 1: Duplicate Request**
        if self.thread_manager.is_duplicate_request(
            last_email.body, past_customer_emails
        ):
            return EmailProcessingResponse(
                status="skipped", reasonForNotProcessing="Duplicate customer request."
            )

        # **Process the last unreplied customer email**
        return self.email_processor.process_email(last_email)
