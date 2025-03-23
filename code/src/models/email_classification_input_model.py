from typing import Any, Dict, List


class EmailClassificationInput:
    """
    Represents a structured input for email classification.
    """

    def __init__(
        self,
        subject: str,
        body: str,
        sender: str,
        date: str,
        attachments: List[str], 
        metadata: Dict[str, Any] = None,
    ):
        self.subject = subject
        self.body = body
        self.sender = sender
        self.date = date
        self.attachments = attachments
        self.metadata = metadata or {}

    def to_dict(self):
        return {
            "subject": self.subject,
            "body": self.body,
            "sender": self.sender,
            "date": self.date,
            "metadata": self.metadata,
        }
