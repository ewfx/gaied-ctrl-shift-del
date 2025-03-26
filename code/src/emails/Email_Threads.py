from models.email_model import Email

email_threads = { 
     "Thread1" : [
     #scenario-2
    Email (
     sender="customer@example.com",
     subject="Request for Adjustment and AU Transfer",
     date="2025-03-22",
     body=(
         "Dear Support Team,\n\n"
         "I would like to request two actions related to my loan account:\n\n"
       
         "1. **Adjustment Request**\n"
         "   I need an adjustment of $2,500 due to an incorrect charge applied on March 15, 2025. "
         "The effective date for this adjustment should be March 20, 2025. The adjustment reason is an "
         "overcharge due to a system error.\n\n"
       
         "2. **AU Transfer Request**\n"
         "   Please transfer $5,000 from Asset Unit 'AU-12345' to 'AU-67890'. This transfer should take "
         "effect immediately.\n\n"
       
         "I have attached the supporting documents for your reference. Let me know if you require any additional information.\n\n"
         "Best regards,\n"
         "[Customer Name]"
     ),
     email_id="102",
     attachments=["adjustment_request.pdf", "au_transfer_details.pdf"],
     thread_id="1010",
     sender_role="customer",
 ),
 ],
     "Thread2": [
         Email(
             sender="customer@example.com",
             subject="Commitment Change Request",
             date="2025-03-22",
             body=("Hello,I need to make a payment for an ongoing fee related to my loan."
                   " The payment details, including the due date and fee period, are attached for your reference. "
                   "Please process the payment accordingly and confirm once completed.Let me know if you need any additional"
                    " information.Best regards,[Customer Name]"),
             email_id="103",
             attachments=["fee_payment_details.pdf"],
             thread_id="1008",
             sender_role="customer",
    ),
     ],

 #scenario -- enquiry about a loan
     "Thread3": [
         # Loan Information Request - enquiry
         Email(
             sender="customer@example.com",
             subject="Loan Information Request",
             date="2025-03-23",
             body=(
                 "Dear Support Team, "
                 "I would like to request details regarding my loan. "
                 "1. **Loan Type:** Business Loan "
                 "2. **Planned Date:** March 25, 2025 "
                 "Could you please provide the necessary details regarding interest rates and repayment terms? "
                 "Best regards, "
                 "[Customer Name]"
             ),
             email_id="104",
             attachments=[],
             thread_id="1009",
             sender_role="customer",
         ),
     ],
    # multiple emails- single thread
     "Thread4": [
         # Money Movement - Outbound
         Email(
             sender="customer@example.com",
             subject="Outbound Money Transfer Request",
             date="2025-03-24",
             body=(
                 "Dear Support Team, "
                 "I would like to request an outbound money transfer as per the following details: "
                 "1. **Transfer Date:** March 26, 2025 "
                 "2. **Recipient Details:** ABC Financial Services "
                 "3. **Transfer Amount:** $10,000 "
                 "4. **Payment Method:** Wire Transfer "
                 "Please confirm once the transaction is processed. "
                 "Best regards, "
                 "[Customer Name]"
             ),
             email_id="105",
             attachments=[],
             thread_id="1011",
             sender_role="customer",
         ),
         Email(
             sender="support@example.com",
             subject="RE: Outbound Money Transfer Request",
             date="2025-03-24",
             body=(
                 "Dear customer, "
                 "The requested transaction has been processed. Please verify from your end and reach out to us in case of any queries."
                 "happy to assist."
             ),
             email_id="106",
             attachments=[],
             thread_id="1011",
             sender_role="support",
         ),
     ],
    "Thread5": [
        # Duplicate Requests in a Single Thread
        Email(
            sender="customer@example.com",
            subject="Payment & Adjustment Request",
            date="2025-03-25",
            body=(
                "Dear Support Team, "
                "I am submitting a request for the following actions on my account: "
                "I need an adjustment of $1,200 for an incorrect charge applied on March 10, 2025. "
                "The effective date for this adjustment should be March 15, 2025. "
                "I have attached supporting documents for your reference. Please let me know if further details are required. "
                "Best regards, "
                "[Customer Name]"
            ),
            email_id="107",
            attachments=["adjustment_proof.pdf"],
            thread_id="1014",
            sender_role="customer",
        ),
         Email(
            sender="support@example.com",
            subject="RE: Payment & Adjustment Request",
            date="2025-03-25",
            body=(
                "Dear Customer"
                "we are in the process of reviewing your request. Please await our response."
            ),
            email_id="109",
            attachments=[],
            thread_id="1014",
            sender_role="support",
        ),

        Email(
            sender="customer@example.com",
            subject="Follow-up: Payment & Adjustment Request",
            date="2025-03-27",
            body=(
                "Dear Support Team, "
                "I am following up on my request regarding the adjustment of $1,200 and the payment of $800. "
                "Could you please provide an update on the processing status? "
                "I appreciate your prompt response. "
                "Best regards, "
                "[Customer Name]"
            ),
            email_id="110",
            attachments=[],
            thread_id="1014",
            sender_role="customer",
        ),
    ],
}


