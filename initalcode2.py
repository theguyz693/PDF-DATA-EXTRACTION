import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import io

pdf_path = "sample.pdf"
doc = fitz.open(pdf_path)

with open("output.txt", "w", encoding="utf-8") as f:
    for i in range(len(doc)):
        page = doc[i]
        pix = page.get_pixmap(dpi=300)
        img_data = pix.tobytes("png")
        image = Image.open(io.BytesIO(img_data))
        
        text = pytesseract.image_to_string(image)
        f.write(f"\n--- OCR Page {i + 1} ---\n")
        f.write(text)

print("Done! OCR text saved to output.txt")
