import re

KEYWORDS = {
    "payslip": 20,
    "pay slip": 20,
    "salary slip": 20,
    "employee id": 15,
    "employee": 10,
    "basic salary": 15,
    "gross salary": 15,
    "net salary": 20,
    "deductions": 10,
    "pay period": 10,
    "pay date": 10,
    "tax": 8,
    "allowance": 8,
    "bank account": 12,
    "earnings": 10,
    "Salary Date":10,
    "Employee Name":10,
    "CNIC":10,
    "Net Pay":20,
    "Net Balance":10
}

THRESHOLD = 35  # minimum score to classify as payslip


def normalize(text: str) -> str:
    return text.lower()


def is_payslip(text: str):
    text = normalize(text)

    score = 0
    matched = []

    for keyword, weight in KEYWORDS.items():
        if keyword in text:
            score += weight
            matched.append(keyword)

    return {
        "is_valid": score >= THRESHOLD,
        "score": score,
        "matched_keywords": matched
    }