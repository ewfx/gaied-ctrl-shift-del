from typing import List, Tuple, Optional


class Email:
    """Class representing an email with sender, subject, date, body, and optional attachments."""

    def __init__(
        self,
        sender: str,
        subject: str,
        date: str,
        body: str,
        attachments: List[str] = None,
        thread_id: Optional[str] = None,
        sender_role: str = "customer",  # Can be "customer" or "support"
    ):
        self.sender = sender
        self.subject = subject
        self.date = date
        self.body = body
        self.attachments = attachments if attachments is not None else []
        self.thread_id = thread_id  # Unique thread ID for grouping related emails
        self.sender_role = sender_role  # "customer" or "support"

    def __repr__(self):
        return f"Email(from={self.sender}, subject={self.subject}, date={self.date}, role={self.sender_role}, attachments={len(self.attachments)})"

    # def print_email(self):
    #     """Nicely formats and prints the email details."""
    #     print("=" * 50)
    #     print(f"📩 From: {self.sender}")
    #     print(f"📅 Date: {self.date}")
    #     print(f"✉️ Subject: {self.subject}")
    #     print("-" * 50)
    #     print(f"📜 Body:\n{self.body[:500]}")  # Limit body length for readability
    #     print("-" * 50)

    #     if self.attachments:
    #         print("📎 Attachments:")
    #         for filename, text in self.attachments:
    #             print(f" - {filename}:")
    #             print(f"   {text[:300]}")  # Limit extracted text for readability
    #             print("-" * 30)
    #     else:
    #         print("📎 Attachments: None")

    #     print("=" * 50, "\n")
