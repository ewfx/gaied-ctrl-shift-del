from flask import Flask, request, jsonify, render_template
from email_service_manager import EmailServiceManager
from email_processor import EmailProcessor
from llm_service import HuggingFaceLLM
from supported_service_requests import supported_service_requests
from Email_Threads import email_threads

app = Flask(__name__)

API_KEY = ""
if not API_KEY:
    raise ValueError("API key not set. Please configure HF_API_KEY as an environment variable.")

llm = HuggingFaceLLM(API_KEY)
email_processor = EmailProcessor(
    llm_service=llm,
    service_request_definitions=supported_service_requests,
    confidence_threshold=0.5,
)
email_service_manager = EmailServiceManager(email_processor)
# Define the API endpoint
@app.route("/api/call_application", methods=["GET"])
def call_application():
    
    response = []
    for thread in email_threads:
        result=email_service_manager.process_email(thread)
        response.append(result.to_dict())
    # result = {"message": "Application called successfully"}
    return jsonify(response)


# Serve the HTML file
@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=False)
