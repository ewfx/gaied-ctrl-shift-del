# 🚀 Email Classification and Data Extraction using Generative AI

## 📌 Table of Contents

- [Introduction](#introduction)
- [Demo](#demo)
- [Inspiration](#inspiration)
- [What It Does](#what-it-does)
- [How We Built It](#how-we-built-it)
- [Challenges We Faced](#challenges-we-faced)
- [How to Run](#how-to-run)
- [Tech Stack](#tech-stack)
- [Team](#team)

## 🎯 Introduction

Our project automates email classification and data extraction using Generative AI, improving efficiency and accuracy while minimizing manual effort. It seamlessly integrates with loan servicing workflows to classify emails, extract key attributes, and auto-route requests to the correct teams.

## 🎥 Demo

- [Live Demo](#) (if applicable)
- [Video Demo](#) (if applicable)
- 📸 Screenshots:

## 💡 Inspiration

Manual triaging of emails in commercial banking loan servicing is slow and error-prone. The motivation for this project was to leverage AI and automation to enhance efficiency, accuracy, and turnaround time while minimizing human effort.

## 🛠 What It Does

This project automates **email classification and data extraction** using **Generative AI (LLMs)** to improve efficiency, accuracy, and turnaround time while minimizing manual effort. The solution:

- Classifies emails into predefined **request types** and **sub-request types**.
- Extracts configurable **key attributes** from emails and attachments of types- ".pdf", ".png", ".jpg", ".jpeg",".xls", ".xlsx",".docx".
- Detects **multiple request types** within a single email and determines the primary intent.
- Implements **priority-based extraction** to prioritize email content over attachments.
- Identifies and flags **duplicate emails** to prevent redundant service requests.

## 🏗 How We Built It

- Developed an **email preprocessor** to clean email text, extract metadata, and process attachments.
- Utilized **mDeBERTa-v3-base-mnli-xnli** for zero-shot email classification and **Mistral-7B-Instruct-v0.1** for extracting structured data from emails and attachments.
- Designed a **priority-based extraction system**, ensuring numerical data is sourced from attachments while request types are primarily identified from the email body.
- Implemented **email thread processing**, allowing classification to consider the full conversation context.
- Built a **robust failure-handling mechanism**, ensuring reliable processing even in cases of API failures or unclassified emails.
- Integrated **duplicate detection**, preventing redundant service requests from being generated for repeated emails.
- Developed a **Flask-based UI**, allowing users to interact with the classification system in real time.

## 🚧 Challenges We Faced

- Ensuring **accurate classification** for diverse email types.
- Handling **multi-request emails** and detecting the primary intent.
- Designing **priority-based extraction** rules that adapt to request types.
- Optimizing **OCR performance** for different document formats.
- Minimizing false positives in **duplicate detection**.

## ▶️ How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/ewfx/gaied-ctrl-shift-del.git
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the email processing script:
   ```bash
   python app.py
   ```
4. View results in the output directory.

## 🛠 Tech Stack

- **Programming Languages:** Python
- **LLMs & NLP Models:** mDeBERTa-v3-base-mnli-xnli, Mistral-7B-Instruct-v0.1
- **Machine Learning Libraries:** Scikit-learn, Hugging Face, LangChain
- **OCR & Data Processing:** Tesseract OCR
- **Web Framework:** Flask (for UI)
- **Deployment:** Flask/FastAPI

## 👥 Team

- Josh Wadhwa
- Monika Kakarla
- Avinash Meka
- Revanth Choudavarapu
- Santosh Allaka

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

