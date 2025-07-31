import pdfplumber
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import os
from docx import Document
import csv

# Set Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Ask user for multiple PDF input
pdf_files = input("Enter PDF filenames separated by commas: ").strip().split(',')

# Ask user for output format
format_choice = input("Choose output format (txt / docx / html / csv): ").strip().lower()

# Create output directory
os.makedirs("output", exist_ok=True)

for pdf_file in pdf_files:
    PDF_PATH = pdf_file.strip()
    OUTPUT_BASENAME = os.path.join("output", os.path.splitext(os.path.basename(PDF_PATH))[0])
    extracted_text = ""
    csv_data = []

    try:
        with pdfplumber.open(PDF_PATH) as pdf:
            for page_number, page in enumerate(pdf.pages):
                try:
                    # Attempt to extract with layout (better formatting)
                    text = page.extract_text(layout=True)
                    if text:
                        extracted_text += f"\n--- Page {page_number+1} ---\n{text}\n"
                        # Prepare CSV row-wise lines
                        csv_data.extend([[line] for line in text.split("\n")])
                    else:
                        # fallback to OCR
                        pix = page.to_image(resolution=300).original
                        text = pytesseract.image_to_string(pix)
                        extracted_text += f"\n--- Page {page_number+1} [OCR] ---\n{text}\n"
                        csv_data.extend([[line] for line in text.split("\n")])
                except Exception as e:
                    extracted_text += f"\n--- Page {page_number+1} ---\n[Error reading this page: {e}]\n"
                    csv_data.append([f"Page {page_number+1} Error: {e}"])
    except Exception as e:
        print(f"Error opening {PDF_PATH}: {e}")
        continue

    # Save in selected format
    if format_choice == "txt":
        with open(f"{OUTPUT_BASENAME}.txt", "w", encoding="utf-8") as f:
            f.write(extracted_text)
        print(f"Saved: {OUTPUT_BASENAME}.txt")

    elif format_choice == "docx":
        doc = Document()
        doc.add_paragraph(extracted_text)
        doc.save(f"{OUTPUT_BASENAME}.docx")
        print(f"Saved: {OUTPUT_BASENAME}.docx")

    elif format_choice == "html":
        html_content = f"<html><body><pre>{extracted_text}</pre></body></html>"
        with open(f"{OUTPUT_BASENAME}.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"Saved: {OUTPUT_BASENAME}.html")

    elif format_choice == "csv":
        with open(f"{OUTPUT_BASENAME}.csv", "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Extracted Text"])
            writer.writerows(csv_data)
        print(f"Saved: {OUTPUT_BASENAME}.csv")

    else:
        print(f"Unsupported format: {format_choice}. Skipped saving for {PDF_PATH}")
