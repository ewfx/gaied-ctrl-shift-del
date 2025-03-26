import uuid
from models.email_model import Email

thread_1 = str(uuid.uuid4())
thread_2 = str(uuid.uuid4())

email_threads = [
     Email(
            sender="customer@example.com",
            subject="Fee Payment Request",
            date="2025-03-22",
            body=(
                "Hello, I want to make a fee payment for my loan. The fee amount due is $1,250, "
                "and I would like to process the payment on 2025-04-01. Please confirm the payment."
            ),
            attachments=[],
            thread_id="1002",
            sender_role="customer"
        ),
        Email(
            sender="support@example.com",
            subject="Re: Fee Payment Request",
            date="2025-03-23",
            body="Your fee payment has been scheduled successfully.",
            attachments=[],
            thread_id="1002",
            sender_role="support"
        ),]

