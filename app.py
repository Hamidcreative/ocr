from flask import Flask, request, jsonify
import os
import json


from ocr import extract_text
from utils import extract_all, similarity,check_expiry,extract_cnic_address
from payslip_utils import is_payslip
from bank_statement_utils import detect_bank_statement

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def load_db():
    with open("reference_data.json") as f:
        return json.load(f)

@app.route("/")
def home():
    return {
        "status": "running"
    }



@app.route("/verify-cnic-no", methods=["POST"])
def verify():

    file = request.files["image"]
    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)
    input_cnic = request.form.get("cnic_no")


    text = extract_text(path)
    allData = extract_all(text)
    ocr_cnic = allData.get("cnic")

    if input_cnic and ocr_cnic and input_cnic == ocr_cnic:
        return jsonify({
            "status": "MATCHED",
            "ocr_cnic": ocr_cnic,
            "input_cnic": input_cnic,
            "OCR Data": allData
        })

    return jsonify({
        "status": "NOT MATCHED",
        "ocr_cnic": ocr_cnic,
        "input_cnic": input_cnic,
        "OCR Data": allData
    })

@app.route("/get-cnic-address", methods=["POST"])
def cnicAddress():
    file = request.files["image"]
    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)
    text = extract_text(path)

    address_lines = extract_cnic_address(text)

    return jsonify({
        "address_lines": address_lines,
        "raw_text": text
    })

@app.route("/verify-cnic-expiry", methods=["POST"])
def expiry():
    file = request.files["image"]
    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)


    text = extract_text(path)
    allData = extract_all(text)

    ocr_expiry = allData.get("expiry")
    result = {
        "OCR Expiry": ocr_expiry,
        "OCR allData": allData,
    }
    if ocr_expiry:
        expiry_status = check_expiry(ocr_expiry)

        result["is_expired"] = expiry_status["is_expired"]
        result["expiring_within_60_days"] = expiry_status["expiring_within_60_days"]
        result["ocr_expiry"] = ocr_expiry

    return jsonify(result)




@app.route("/verify-payslip", methods=["POST"])
def payslip():
    file = request.files["image"]
    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)

    text = extract_text(path)

    allData = is_payslip(text)
    return jsonify(allData)

@app.route("/verify-bank-statement", methods=["POST"])
def verify_bank_statement():
    DB = load_db()
    file = request.files["image"]
    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)

    text = extract_text(path)

    allData = detect_bank_statement(text)
    return jsonify(allData)

if __name__ == "__main__":
    app.run(debug=True)