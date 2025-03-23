from typing import List, Optional, Tuple


from typing import List, Tuple


class Email:
    """Class representing an email with sender, subject, date, body, and optional attachments."""

    def __init__(
        self,
        sender: str,
        subject: str,
        date: str,
        body: str,
        attachments: List[Tuple[str, bytes]] = None,
    ):
        self.sender = sender
        self.subject = subject
        self.date = date
        self.body = body
        self.attachments = (
            attachments if attachments is not None else []
        )  # Default to an empty list if None is provided

    def __repr__(self):
        return f"Email(from={self.sender}, subject={self.subject}, date={self.date}, attachments={len(self.attachments)})"

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
