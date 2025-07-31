# PDF-DATA-EXTRACTION
# PDF Text Extractor with OCR & Multi-Format Output

Extracts text from PDFs exports output files to `.txt`, `.docx`, `.html`, and `.csv`.

## Features

- Extracts text with layout using `pdfplumber`
- Falls back to `pytesseract` OCR for scanned pages
- Saves output in TXT, DOCX, HTML, and CSV formats

## Requirements

- `pdfplumber`, `pytesseract`, `Pillow`, `python-docx`,`fitz`
- Tesseract-OCR installed (e.g. `C:\Program Files\Tesseract-OCR\tesseract.exe`)
- pip install pdfplumber pymupdf pytesseract Pillow pandas layoutparser pdf2image beautifulsoup4 opencv-python
- pip install pdfplumber pymupdf pytesseract Pillow pandas

## Note
requires the pdf file to be in the same folder 
best outputs with invoice,admit cards,etc
poor with data/table heavy files like marksheets
