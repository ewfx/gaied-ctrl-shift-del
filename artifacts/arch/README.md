ewfx/gaied-ctrl-shift-del  
├── .gitignore               # Ignore unnecessary files  
├── LICENSE                  # License file  
├── README.md                # Documentation  
├── requirements.txt         # Required dependencies  
├── .vscode/                 
│   ├── launch.json  
│   └── settings.json  
├── artifacts/               # Sample artifacts & documents  
│   ├── Loan_Adjustment_Request.docx  
│   ├── Loan_Adjustment_Request.pdf  
│   ├── adjustment_request.pdf  
│   ├── arch/  
│   │   └── README.md  
│   ├── au_transfer_details.pdf  
│   ├── commitment_change_details.pdf  
│   ├── demo/  
│   │   └── README.md  
├── code/                    # Source code directory  
│   ├── src/                 # Main source code  
│   │   ├── app.py           # Flask UI application  
│   │   ├── attachment_processor.py # Processes file attachments  
│   │   ├── email_preprocessor.py  # Cleans and preps emails  
│   │   ├── email_processor.py     # Handles email classification  
│   │   ├── email_service_manager.py  # Manages email services  
│   │   ├── email_thread_manager.py  # Handles email threads  
│   │   ├── llm_service.py     # Integrates LLM models  
│   │   ├── main.py            # Main execution script  
│   │   ├── supported_service_requests.py  # Request type definitions  
│   │   ├── emails/            # Sample email data  
│   │   ├── models/            # ML/NLP models and configurations  
│   │   └── templates/         # UI templates  
│   ├── test/                  # Testing scripts  
│   │   └── README.md  
