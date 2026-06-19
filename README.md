# CNIC OCR & Document Verification System

A Flask-based OCR microservice for extracting and verifying information from CNICs and detecting financial documents such as payslips and bank statements.

## Features

### CNIC Data Extraction
Extracts the following information from CNIC images or PDFs:

- CNIC Number
- Name
- Father Name
- Date of Birth
- Issue Date
- Expiry Date

### CNIC Verification
- Verify CNIC number against reference data (database/JSON)
- Check whether CNIC is expired or will expire within the next 60 days

### Document Detection
- Payslip detection
- Bank statement detection

### Name Matching
- Compare extracted names with reference data
- Similarity scoring using RapidFuzz

### OCR Processing
- OCR using Tesseract
- Image preprocessing using OpenCV
- PDF support

---

## Technology Stack

- Python
- Flask
- Tesseract OCR
- OpenCV
- RapidFuzz
- PDF Processing Libraries

---

## API Endpoints

### Verify CNIC Number

```http
POST /verify-cnic-no
```

Verifies whether the extracted CNIC number exists in the reference database.

---

### Verify CNIC Expiry

```http
POST /verify-cnic-expiry
```

Checks whether the CNIC is valid and whether the expiry date is within 60 days.

---

### Verify Payslip

```http
POST /verify-payslip
```

Detects whether the uploaded document is a payslip.

---

### Verify Bank Statement

```http
POST /verify-bank-statement
```

Detects whether the uploaded document is a bank statement.

---

## Project Structure

```text
project/
│
├── .venv
├── .env
├── app.py
├── ocr.py
├── utils.py
├── bank_statement_utils.py
├── payslip_utils.py
├── reference_data.json
├── uploads/
├── requirements.txt
└── config.py
└── README.md

```

---

## Installation

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

Mac/Linux:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Application

```bash
python app.py
```

Server will start at:

```text
http://127.0.0.1:5000
```

---

## Future Enhancements

- AI-based document classification
- Face verification with CNIC
- Laravel integration
- Docker deployment
- Multi-document support
- Confidence scoring for extracted fields

---

## Author



Python OCR Microservice for CNIC Verification, Payslip Detection, and Bank Statement Detection.