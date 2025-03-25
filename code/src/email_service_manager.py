from models.email_model import Email
from email_thread_manager import EmailThreadManager
from email_processor import EmailProcessor


class EmailServiceManager:
    def __init__(self, email_processor: EmailProcessor):
        self.email_processor = email_processor
        self.thread_manager = EmailThreadManager()

    def process_email(self, email: Email):
        """Main method to process emails, handling threads and duplicates."""
        self.thread_manager.add_email(email)  # Add email to thread

        # Get last unreplied customer email
        last_email, past_customer_emails = (
            self.thread_manager.get_last_unreplied_customer_email(
                email.thread_id or email.sender
            )
        )

        if not last_email:
            print(f"Skipping email: {email.subject} (No open customer request).")
            return None

        # Check for duplicate request
        if self.thread_manager.is_duplicate_request(
            last_email.body, past_customer_emails
        ):
            print(f"Skipping email: {email.subject} (Duplicate request).")
            return None

        # Process the last unreplied customer email
        return self.email_processor.process_email(last_email)
