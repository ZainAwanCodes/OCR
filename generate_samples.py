from PIL import Image, ImageDraw, ImageFont
import os

def get_font(size=28):
    # Try to load a clean Windows system font, fallback to default
    font_paths = [
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/calibri.ttf",
        "C:/Windows/Fonts/cour.ttf",  # Courier - monospaced, great for OCR
    ]
    for fp in font_paths:
        if os.path.exists(fp):
            return ImageFont.truetype(fp, size)
    return ImageFont.load_default()

def create_sample_image(filename, lines, size=(700, 400)):
    img = Image.new('RGB', size, color='white')
    d = ImageDraw.Draw(img)
    font = get_font(28)
    
    y_text = 40
    for line in lines:
        d.text((50, y_text), line, fill=(0, 0, 0), font=font)
        y_text += 55

    img.save(filename)
    print(f"Created {filename}")

if __name__ == "__main__":
    # 1. Valid Claim Images
    
    create_sample_image("Sample_ID.png", [
        "Health Insurance ID Card",
        "------------------------",
        "Name: Alice Smith",
        "ID Number: INS-987654321",
        "DOB: 1990-01-01"
    ])
    
    create_sample_image("Sample_Premium.png", [
        "Premium Policy Details",

        "------------------------",
        "Name: Alice Smith",
        "Status: Active",
        "Coverage Limit: $10,000.00"
    ])
    
    create_sample_image("Sample_Invoice.png", [
        "General Hospital - Medical Invoice",
        "------------------------",
        "Patient Name: Alice Smith",
        "Patient ID: INS-987654321",
        "Total Amount: $2,500.00"
    ])

    # 2. Rejected Claim Images (Exceeds Limit & Unpaid)
    create_sample_image("Rejected_Premium.png", [
        "Premium Policy Details",
        "------------------------",
        "Name: Alice Smith",
        "Status: Unpaid",
        "Coverage Limit: $5,000.00"
    ])
    
    create_sample_image("Rejected_Invoice.png", [
        "General Hospital - Medical Invoice",
        "------------------------",
        "Patient Name: Alice Smith",
        "Patient ID: INS-987654321",
        "Total Amount: $12,500.00"
    ])
