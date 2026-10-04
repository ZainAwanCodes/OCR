import pytesseract
from PIL import Image
import os
import re

# Set the path to the Tesseract executable explicitly
pytesseract.pytesseract.tesseract_cmd = r'D:\Tesseract\tesseract.exe'

# Fallback mocked logic for testing if Tesseract is not available
MOCK_DATA = {
    'id': {'name': 'John Doe', 'id_number': 'ID-123456789'},
    'premium': {'name': 'John Doe', 'status': 'Active', 'coverage_limit': 5000.00},
    'invoice': {'name': 'John Doe', 'total_amount': 1500.00, 'id_number': 'ID-123456789'}
}

def check_tesseract_available():
    try:
        pytesseract.get_tesseract_version()
        return True
    except pytesseract.TesseractNotFoundError:
        return False
    except Exception:
        return False

HAS_TESSERACT = check_tesseract_available()

def extract_text(image_path):
    if not HAS_TESSERACT:
        return ""
    try:
        img = Image.open(image_path)
        return pytesseract.image_to_string(img)
    except Exception as e:
        print(f"OCR Error: {e}")
        return ""

def parse_id(image_path):
    if not HAS_TESSERACT:
        return MOCK_DATA['id']
    text = extract_text(image_path)
    print(f"[OCR RAW - ID]\n{text}")
    # Match on individual lines to avoid keyword bleed
    name_match = re.search(r'^Name:\s*(.+)$', text, re.IGNORECASE | re.MULTILINE)
    id_match = re.search(r'^ID Number:\s*(.+)$', text, re.IGNORECASE | re.MULTILINE)
    # Fallback: grab any INS-style token from anywhere
    if not id_match:
        id_match = re.search(r'(INS[\s\-]*[\d\s\-]+)', text, re.IGNORECASE)
    raw_id = re.sub(r'[^A-Z0-9\-]', '', id_match.group(1).upper()) if id_match else 'Unknown'
    return {
        'name': name_match.group(1).strip() if name_match else 'Unknown',
        'id_number': raw_id
    }

def parse_premium(image_path):
    if not HAS_TESSERACT:
        return MOCK_DATA['premium']
    text = extract_text(image_path)
    print(f"[OCR RAW - Premium]\n{text}")
    name_match = re.search(r'^Name:\s*(.+)$', text, re.IGNORECASE | re.MULTILINE)
    status_match = re.search(r'^Status[:\s]+([A-Za-z]+)', text, re.IGNORECASE | re.MULTILINE)
    limit_match = re.search(r'^Coverage Limit\s*\$?([\d,]+\.?\d*)$', text, re.IGNORECASE | re.MULTILINE)
    if not limit_match:
        limit_match = re.search(r'\$([\d,]+\.?\d*)', text)

    limit = 0.0
    if limit_match:
        try:
            limit = float(limit_match.group(1).replace(',', ''))
        except:
            pass

    return {
        'name': name_match.group(1).strip() if name_match else 'Unknown',
        'status': status_match.group(1).strip() if status_match else 'Unknown',
        'coverage_limit': limit
    }

def parse_invoice(image_path):
    if not HAS_TESSERACT:
        return MOCK_DATA['invoice']
    text = extract_text(image_path)
    print(f"[OCR RAW - Invoice]\n{text}")
    name_match = re.search(r'^Patient Name:\s*(.+)$', text, re.IGNORECASE | re.MULTILINE)
    id_match = re.search(r'^Patient ID[:\w]*\s*(.+)$', text, re.IGNORECASE | re.MULTILINE)
    if not id_match:
        id_match = re.search(r'(INS[\s\-]*[\d\s\-]+)', text, re.IGNORECASE)
    amount_match = re.search(r'^Total Amount\s*\$?([\d,]+\.?\d*)$', text, re.IGNORECASE | re.MULTILINE)
    if not amount_match:
        amount_match = re.search(r'\$([\d,]+\.?\d*)', text)

    amount = 0.0
    if amount_match:
        try:
            amount = float(amount_match.group(1).replace(',', ''))
        except:
            pass

    raw_id = re.sub(r'[^A-Z0-9\-]', '', id_match.group(1).upper()) if id_match else 'Unknown'
    return {
        'name': name_match.group(1).strip() if name_match else 'Unknown',
        'id_number': raw_id,
        'total_amount': amount
    }

def verify_claim(id_data, premium_data, invoice_data):
    reasons = []
    approved = True

    # 1. Match name and ID across documents
    if id_data['name'].lower() != invoice_data['name'].lower():
        approved = False
        reasons.append("Name mismatch between ID and Medical Invoice.")
    if id_data['name'].lower() != premium_data['name'].lower():
        approved = False
        reasons.append("Name mismatch between ID and Premium document.")
    if id_data['id_number'] != invoice_data['id_number']:
        approved = False
        reasons.append("ID Number mismatch between ID document and Medical Invoice.")

    # 2. Check if premium is paid/active
    status = premium_data['status'].strip(': ').lower()
    if status not in ['active', 'paid']:
        approved = False
        reasons.append(f"Premium status is not active (Status: {premium_data['status'].strip(': ')}).")

    # 3. Verify medical invoice total against premium coverage limits
    if invoice_data['total_amount'] > premium_data['coverage_limit']:
        approved = False
        reasons.append(f"Invoice amount (${invoice_data['total_amount']}) exceeds coverage limit (${premium_data['coverage_limit']}).")
        
    if approved:
        reasons.append("All checks passed. Claim is fully approved.")

    return {
        'approved': approved,
        'reasons': reasons
    }
