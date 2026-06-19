import re

BANK_KEYWORDS = {
    "bank statement": 25,
    "statement of account": 25,
    "account summary": 20,
    "opening balance": 20,
    "closing balance": 20,
    "available balance": 15,
    "debit": 10,
    "credit": 10,
    "transaction": 15,
    "withdrawal": 12,
    "deposit": 12,
    "iban": 20,
    "account number": 15,
    "branch code": 10,
    "hbl": 12,
    "ubl": 12,
    "meezan bank": 15,
    "mcb": 12
}

THRESHOLD = 35  # minimum score to classify as payslip


def normalize(text: str) -> str:
    return text.lower()


def detect_bank_statement(text):
    text = normalize(text)

    score = 0
    matched = []

    for keyword, weight in BANK_KEYWORDS.items():
        if keyword in text:
            score += weight
            matched.append(keyword)

    return {
        "is_valid": score >= 40,
        "score": score,
        "matched_keywords": matched
    }