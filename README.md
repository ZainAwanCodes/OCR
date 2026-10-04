# 🏥 AutoClaim — OCR Insurance Claim Verifier

AutoClaim is a Flask-based web application that uses **OCR (Optical Character Recognition)** to automatically extract and verify insurance claim documents. Upload three document images — an **ID Card**, a **Premium/Policy document**, and a **Medical Invoice** — and the system instantly tells you whether the insurance claim is **Approved ✅** or **Rejected ❌**.

---

## 🖼️ How It Works

The system reads three documents using Tesseract OCR, extracts key fields, and runs the following verification checks:

| Check | Description |
|-------|-------------|
| **Name Match** | Patient name must match across all three documents |
| **ID Match** | Insurance ID on the Medical Invoice must match the ID Card |
| **Premium Status** | Policy status must be `Active` or `Paid` |
| **Coverage Limit** | Invoice total must not exceed the policy's coverage limit |

If **all checks pass** → Claim is **Approved**.  
If **any check fails** → Claim is **Rejected** with detailed reasons.

---

## 📁 Sample Images

The repository includes ready-to-use sample images for testing:

| File | Type | Expected Result |
|------|------|-----------------|
| `Sample_ID.png` | ID Card | ✅ Valid ID |
| `Sample_Premium.png` | Premium Document | ✅ Active policy |
| `Sample_Invoice.png` | Medical Invoice | ✅ Within coverage limit |
| `Rejected_Premium.png` | Premium Document | ❌ Inactive/expired policy |
| `Rejected_Invoice.png` | Medical Invoice | ❌ Amount exceeds coverage |
| `Id.png` | ID Card | Test ID |
| `Premium.png` | Premium Document | Test premium |
| `Medical-Invoice.png` | Medical Invoice | Test invoice |

> **Tip:** To test an **Approved** claim, use `Sample_ID.png` + `Sample_Premium.png` + `Sample_Invoice.png`.  
> To test a **Rejected** claim, try swapping in `Rejected_Premium.png` or `Rejected_Invoice.png`.

---

## 🚀 Getting Started

### Prerequisites

Make sure you have the following installed:

- **Python 3.8+** → [Download](https://www.python.org/downloads/)
- **Tesseract OCR** → [Download for Windows](https://github.com/UB-Mannheim/tesseract/wiki)
- **Git** → [Download](https://git-scm.com/)

> ⚠️ After installing Tesseract, note its installation path (e.g., `D:\Tesseract\tesseract.exe`). You'll need it in the next step.

---

### 1. Clone the Repository

```bash
git clone https://github.com/ZainAwanCodes/OCR.git
cd OCR
```

---

### 2. Create and Activate a Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate

# Activate it (Mac/Linux)
source venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install flask pytesseract pillow werkzeug
```

---

### 4. Configure Tesseract Path

Open `ocr_engine.py` and update line 7 with your Tesseract installation path:

```python
# ocr_engine.py — Line 7
pytesseract.pytesseract.tesseract_cmd = r'D:\Tesseract\tesseract.exe'
```

> Common paths:
> - **Windows:** `C:\Program Files\Tesseract-OCR\tesseract.exe`
> - **Mac (Homebrew):** `/usr/local/bin/tesseract`
> - **Linux:** `/usr/bin/tesseract`

---

### 5. Run the Application

```bash
python app.py
```

You should see:

```
* Running on http://127.0.0.1:5000
* Debug mode: on
```

Open your browser and go to **http://127.0.0.1:5000**

---

## 🧪 Testing a Claim

1. Open the app in your browser at `http://127.0.0.1:5000`
2. Upload the three required images:
   - **ID Card** → e.g., `Sample_ID.png`
   - **Premium Document** → e.g., `Sample_Premium.png`
   - **Medical Invoice** → e.g., `Sample_Invoice.png`
3. Click **"Verify Claim"**
4. The system extracts text from each image via OCR and runs verification
5. Results show:
   - Extracted data from each document
   - **✅ Claim Approved** or **❌ Claim Rejected**
   - Detailed reasons for the decision

---

## 📂 Project Structure

```
OCR/
│
├── app.py                  # Flask app — routes and API
├── ocr_engine.py           # OCR extraction & claim verification logic
├── generate_samples.py     # Script to regenerate sample test images
├── test_ocr.py             # Quick OCR test script
│
├── templates/
│   └── index.html          # Frontend UI
│
├── static/
│   └── style.css           # Styles
│
├── uploads/                # Uploaded images (auto-created, not tracked)
│
├── Sample_ID.png           # ✅ Sample ID Card image
├── Sample_Premium.png      # ✅ Sample Premium document
├── Sample_Invoice.png      # ✅ Sample Medical Invoice
├── Rejected_Premium.png    # ❌ Rejected premium (inactive status)
├── Rejected_Invoice.png    # ❌ Rejected invoice (exceeds limit)
├── Id.png                  # Test ID image
├── Premium.png             # Test premium image
├── Medical-Invoice.png     # Test medical invoice
│
└── README.md
```

---

## ⚙️ Verification Logic

```
ID Card Name  ==  Premium Document Name  ==  Medical Invoice Patient Name
                                   AND
ID Card Number  ==  Medical Invoice Patient ID
                                   AND
Premium Status  ==  "Active" or "Paid"
                                   AND
Invoice Total Amount  <=  Coverage Limit
```

All four conditions must be **true** for a claim to be approved.

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, Flask |
| OCR Engine | Tesseract OCR via `pytesseract` |
| Image Processing | Pillow (PIL) |
| Frontend | HTML, CSS, Vanilla JavaScript |
| Font | Google Fonts — Outfit |

---

## 📝 Notes

- The app has a **mock/fallback mode**: if Tesseract is not found, it uses pre-defined mock data so you can still test the UI without OCR.
- Uploaded images are stored temporarily in the `uploads/` folder with unique filenames to avoid conflicts.
- Maximum upload size is **16 MB** per image.

---

## 👤 Author

**Muhammad Zain Awan**  
📧 zain.202404864@gcuf.edu.pk  
🔗 [GitHub — ZainAwanCodes](https://github.com/ZainAwanCodes)
