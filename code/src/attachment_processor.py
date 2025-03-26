import pdfplumber
import pytesseract
from PIL import Image
import docx
import pandas as pd
import os
import io


class AttachmentProcessor:
    """
    Handles extraction of text from email attachments in a specified folder.
    """

    def __init__(self, folder: str, image_ocr_enabled=True):
        self.folder = os.path.abspath(folder)  # Convert to absolute path  # Base folder where attachments are stored
        self.image_ocr_enabled = image_ocr_enabled  # Enable OCR for images if needed

    def extract_text_from_attachment(self, file_name: str) -> str:
        """
        Reads the file from the specified folder and extracts text based on its type.
        """
        file_path = os.path.join(self.folder, file_name)
        file_path = os.path.normpath(file_path)
        if not os.path.exists(file_path):
            return f"Error: File not found - {file_path}"

        file_extension = os.path.splitext(file_name)[-1].lower()

        try:
            with open(file_path, "rb") as file:
                file_bytes = file.read()
        except Exception as e:
            return f"Error reading file: {str(e)}"

        try:
            if file_extension == ".pdf":
                return self._extract_text_from_pdf(file_bytes)
            elif file_extension in [".png", ".jpg", ".jpeg"]:
                return self._extract_text_from_image(file_bytes)
            elif file_extension == ".docx":
                return self._extract_text_from_docx(file_bytes)
            elif file_extension in [".xls", ".xlsx"]:
                return self._extract_text_from_excel(file_bytes)
            else:
                return "Unsupported file format"
        except Exception as e:
            return f"Error processing file: {str(e)}"

    def _extract_text_from_pdf(self, file_bytes: bytes) -> str:
        """Extracts text from a PDF file using pdfplumber."""
        text = ""
        try:
            with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
                for page in pdf.pages:
                    extracted_text = page.extract_text()
                    if extracted_text:
                        text += extracted_text + "\n"
        except Exception as e:
            return f"Error reading PDF: {str(e)}"
        return text.strip() if text.strip() else "No extractable text found in PDF"

    def _extract_text_from_image(self, file_bytes: bytes) -> str:
        """Extracts text from an image file using OCR (Tesseract)."""
        if not self.image_ocr_enabled:
            return "OCR processing disabled"
        try:
            image = Image.open(io.BytesIO(file_bytes))
            return pytesseract.image_to_string(image)
        except Exception as e:
            return f"Error processing image: {str(e)}"

    def _extract_text_from_docx(self, file_bytes: bytes) -> str:
        """Extracts text from a Word (.docx) file using python-docx."""
        try:
            doc = docx.Document(io.BytesIO(file_bytes))
            return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
        except Exception as e:
            return f"Error reading DOCX: {str(e)}"

    def _extract_text_from_excel(self, file_bytes: bytes) -> str:
        """Extracts text from an Excel (.xls/.xlsx) file using pandas."""
        try:
            excel_data = pd.ExcelFile(io.BytesIO(file_bytes))
            text = []
            for sheet_name in excel_data.sheet_names:
                df = excel_data.parse(sheet_name)
                text.append(f"Sheet: {sheet_name}\n{df.to_string(index=False)}")
            return "\n\n".join(text)
        except Exception as e:
            return f"Error reading Excel: {str(e)}"
