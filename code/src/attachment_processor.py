import pdfplumber
import pytesseract
from PIL import Image
import docx
import pandas as pd
import os
import io
from typing import List, Dict, Tuple

class AttachmentProcessor:
    """
    Handles extraction of text from email attachments.
    """

    def __init__(self, image_ocr_enabled=True):
        self.image_ocr_enabled = image_ocr_enabled  # Enable OCR for images if needed

    def extract_text_from_attachment(self, file_name: str, file_bytes: bytes) -> str:
        """
        Extracts text from different types of attachments.
        """
        file_extension = os.path.splitext(file_name)[-1].lower()

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

    def _extract_text_from_pdf(self, file_bytes: bytes) -> str:
        """Extracts text from a PDF file using pdfplumber."""
        text = ""
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        return text.strip()

    def _extract_text_from_image(self, file_bytes: bytes) -> str:
        """Extracts text from an image file using OCR (Tesseract)."""
        if not self.image_ocr_enabled:
            return "OCR processing disabled"
        image = Image.open(io.BytesIO(file_bytes))
        return pytesseract.image_to_string(image)

    def _extract_text_from_docx(self, file_bytes: bytes) -> str:
        """Extracts text from a Word (.docx) file using python-docx."""
        doc = docx.Document(io.BytesIO(file_bytes))
        return "\n".join([p.text for p in doc.paragraphs])

    def _extract_text_from_excel(self, file_bytes: bytes) -> str:
        """Extracts text from an Excel (.xlsx) file using pandas."""
        df = pd.read_excel(io.BytesIO(file_bytes))
        return df.to_string(index=False)

