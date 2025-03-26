import json
from flask import Flask, request, jsonify, render_template
from email_service_manager import EmailServiceManager
from email_processor import EmailProcessor
from llm_service import HuggingFaceLLM
from supported_service_requests import supported_service_requests
from emails.Email_Threads import email_threads

app = Flask(__name__)

API_KEY = ""
if not API_KEY:
    raise ValueError(
        "API key not set. Please configure HF_API_KEY as an environment variable."
    )

llm = HuggingFaceLLM(API_KEY)
email_processor = EmailProcessor(
    llm_service=llm,
    service_request_definitions=supported_service_requests,
    confidence_threshold=0.5,
)
email_service_manager = EmailServiceManager(email_processor)


# Define the API endpoint
@app.route("/api/call_application", methods=["POST"])
def call_application():
    data = request.get_json()
    scenario_id = data.get("scenario_id")  # Extract scenario_id from request body

    if not scenario_id:
        return jsonify({"error": "Missing scenario_id"}), 400

    # Fetch filtered email threads based on scenario_id
    filtered_threads = email_threads.get(f"Thread{scenario_id}")

    if not filtered_threads:
        return jsonify({"error": f"No emails found for scenario {scenario_id}"}), 404

    # Convert each email thread to a dictionary
    emails_json = [thread.to_dict() for thread in filtered_threads]

    # Process emails and generate response
    processing_response = [
        email_service_manager.process_email(thread).to_dict()
        for thread in filtered_threads
    ]

    return jsonify({"emails": emails_json, "processing_response": processing_response})


@app.route("/api/get_configured_service_requests", methods=["GET"])
def get_supported_service_requests():
    return jsonify({"request_types": {key: value.to_dict() for key, value in supported_service_requests.items()}})


# Serve the HTML file
@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=False)
