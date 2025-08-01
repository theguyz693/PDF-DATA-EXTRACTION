import pdfplumber
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import os
from docx import Document
import csv

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


pdf_files = input("Enter PDF filenames separated by commas: ").strip().split(',')


format_choice = input("Choose output format (txt / docx / html / csv): ").strip().lower()

os.makedirs("output", exist_ok=True)

for pdf_file in pdf_files:
    PDF_PATH = pdf_file.strip()
    OUTPUT_BASENAME = os.path.join("output", os.path.splitext(os.path.basename(PDF_PATH))[0])
    extracted_text = ""
    csv_data = []

    try:
        with pdfplumber.open(PDF_PATH) as pdf:
            for page_number, page in enumerate(pdf.pages):
                page_text = f"\n--- Page {page_number + 1} ---\n"

                # Extract embedded text
                text = page.extract_text(layout=True)
                if text:
                    page_text += f"\n[Extracted Text]\n{text.strip()}\n"
                    csv_data.extend([[line] for line in text.split("\n")])
                else:
                    page_text += "\n[Extracted Text] None found\n"

                # Run OCR on image of the page
                try:
                    pix = page.to_image(resolution=300).original
                    ocr_text = pytesseract.image_to_string(pix)
                    page_text += f"\n[OCR Text]\n{ocr_text.strip()}\n"
                    csv_data.extend([[line] for line in ocr_text.split("\n")])
                except Exception as ocr_error:
                    page_text += f"\n[OCR Error] {ocr_error}\n"
                    csv_data.append([f"OCR Error: {ocr_error}"])

                extracted_text += page_text

    except Exception as e:
        print(f"Error opening {PDF_PATH}: {e}")
        continue

    # formats
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
