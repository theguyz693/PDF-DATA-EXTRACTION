import pdfplumber
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import os
from docx import Document  # for .docx support

# Set Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

PDF_PATH = "sample.pdf"  # change this to your actual file name
OUTPUT_BASENAME = os.path.splitext(PDF_PATH)[0]

# Ask user for output format
format_choice = input("Choose output format (txt / docx / html): ").strip().lower()

extracted_text = ""

with pdfplumber.open(PDF_PATH) as pdf:
    for page_number, page in enumerate(pdf.pages):
        try:
            text = page.extract_text()
            if text:
                extracted_text += f"\n--- Page {page_number+1} ---\n{text}\n"
            else:
                # fallback to OCR
                pix = page.to_image(resolution=300).original
                text = pytesseract.image_to_string(pix)
                extracted_text += f"\n--- Page {page_number+1} [OCR] ---\n{text}\n"
        except Exception as e:
            extracted_text += f"\n--- Page {page_number+1} ---\n[Error reading this page: {e}]\n"

# Save output
if format_choice == "txt":
    with open(f"{OUTPUT_BASENAME}.txt", "w", encoding="utf-8") as f:
        f.write(extracted_text)
    print(f"Saved as {OUTPUT_BASENAME}.txt")

elif format_choice == "docx":
    doc = Document()
    doc.add_paragraph(extracted_text)
    doc.save(f"{OUTPUT_BASENAME}.docx")
    print(f"Saved as {OUTPUT_BASENAME}.docx")

elif format_choice == "html":
    html_content = f"<html><body><pre>{extracted_text}</pre></body></html>"
    with open(f"{OUTPUT_BASENAME}.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Saved as {OUTPUT_BASENAME}.html")

else:
    print("Unsupported format selected. No file saved.")
