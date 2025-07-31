import pdfplumber
import pytesseract
from PIL import Image
import os

# Set Tesseract path for Windows (change if yours is different)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

input_pdf = "a.pdf"
output_txt = "output.txt"

def extract_text_from_pdf(pdf_path):
    full_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            print(f"Processing page {i+1}...")
            text = page.extract_text()
            if text and text.strip():
                full_text += f"\n--- Page {i+1} (text) ---\n"
                full_text += text
            else:
                # Page has no text — try OCR
                image = page.to_image(resolution=300).original
                ocr_text = pytesseract.image_to_string(image)
                full_text += f"\n--- Page {i+1} (OCR) ---\n"
                full_text += ocr_text
    return full_text

if not os.path.exists(input_pdf):
    print(f"❌ PDF file '{input_pdf}' not found in the folder.")
else:
    text_result = extract_text_from_pdf(input_pdf)
    with open(output_txt, "w", encoding="utf-8") as f:
        f.write(text_result)
    print(f"✅ Text extracted and saved to '{output_txt}'.")

