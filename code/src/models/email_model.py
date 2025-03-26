from typing import List, Tuple, Optional


class Email:
    """Class representing an email with sender, subject, date, body, and optional attachments."""

    def __init__(
        self,
        sender: str,
        subject: str,
        date: str,
        body: str,
        email_id:  str,
        attachments: List[str] = None,
        thread_id: Optional[str] = None,
        sender_role: str = "customer",  # Can be "customer" or "support"
    ):
        self.sender = sender
        self.subject = subject
        self.date = date
        self.body = body
        self.attachments = attachments if attachments is not None else []
        self.email_id = email_id
        self.thread_id = thread_id  # Unique thread ID for grouping related emails
        self.sender_role = sender_role  # "customer" or "support"

    def __repr__(self):
        return f"Email(from={self.sender}, subject={self.subject}, date={self.date}, role={self.sender_role}, attachments={len(self.attachments)})"

    def to_dict(self) -> dict:
        return {
            "sender": self.sender,
            "subject": self.subject,
            "date": self.date,
            "body": self.body,
            "email_id": self.email_id,
            "attachments": self.attachments,
            "thread_id": self.thread_id,
            "sender_role": self.sender_role
        }
