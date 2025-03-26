from models.email_model import Email

email_threads = [
    #scenario 1- create new request if it is not duplicate
   Email(
       sender="customer@example.com",
       subject="Commitment Change Request",
       date="2025-03-22",
       body=("Hello,I would like to request a change to my loan commitment. Due to recent financial adjustments, I need to decrease the commitment amount. I’ve attached the relevant details for your reference.Please review and let me know if any further information is required.Best regards,[Customer Name]"),
       attachments=["commitment_change_details.pdf"],
       thread_id="1008",
       sender_role="customer",
   ),]

