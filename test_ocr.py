import pytesseract
from PIL import Image

def test_ocr(image_path):
    print(f"--- OCR for {image_path} ---")
    try:
        text = pytesseract.image_to_string(Image.open(image_path))
        print(text)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Point to tesseract executable if needed (e.g. windows)
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    test_ocr("Id.png")
    test_ocr("Premium.png")
    test_ocr("Medical-Invoice.png")
