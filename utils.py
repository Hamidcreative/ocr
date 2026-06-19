import re
from rapidfuzz import fuzz
from datetime import datetime, timedelta
from datetime import datetime

def clean_lines(text):
    lines = text.split("\n")
    return [l.strip() for l in lines if l.strip()]


def find_after_keyword(lines, keyword):
    """
    Finds value in next lines after keyword
    """
    for i, line in enumerate(lines):
        if keyword.lower() in line.lower():
            # check next 1–3 lines for actual value
            for j in range(1, 4):
                if i + j < len(lines):
                    candidate = lines[i + j].strip()
                    if len(candidate) > 3:
                        return candidate
    return None


def extract_cnic(text):
    match = re.search(
        r"\d{5}\s*[- ]\s*\d{7}\s*[- ]\s*\d",
        text
    )

    if match:
        cnic = re.sub(r"\D", "", match.group())

        return f"{cnic[:5]}-{cnic[5:12]}-{cnic[12]}"



def extract_dob(text):
    match = re.search(r"\d{2}[./-]\d{2}[./-]\d{4}", text)
    return match.group() if match else None




def get_all_dates(text):

    dates = []
    for token in text.replace(":", " ").replace("|", " ").split():
        token = token.replace(",", ".")
        if token.count(".") == 2:
            dates.append(token)

    return list(dict.fromkeys(dates))  # remove duplicates
def assign_dates(text):
    dates = get_all_dates(text)

    if len(dates) < 2:
        return None, None, None

    dob = dates[0]
    issue = dates[1]
    expiry = dates[2] if len(dates) > 2 else None

    # 🔥 FIX: validate logic
    if expiry and issue and expiry == issue:
        expiry = None

    return dob, issue, expiry
def validate_dates(dob, issue, expiry):

    try:
        dob_dt = datetime.strptime(dob, "%d.%m.%Y")
        issue_dt = datetime.strptime(issue, "%d.%m.%Y")
        expiry_dt = datetime.strptime(expiry, "%d.%m.%Y")

        if not (dob_dt < issue_dt < expiry_dt):
            return dob, issue, expiry

    except Exception:
        pass

    return dob, issue, expiry

def extract_name(text):
    lines = clean_lines(text)
    val = find_after_keyword(lines, "name")

    if val and "father" not in val.lower():
        return val
    return None


def extract_father_name(text):
    lines = clean_lines(text)
    return find_after_keyword(lines, "father")


def extract_all(text):
    dob, issue, expiry = assign_dates(text)
    dob, issue, expiry = validate_dates(dob, issue, expiry)

    if "lifetime" in text.lower():
        expiry = "LIFETIME"
    return {
        "cnic": extract_cnic(text),
        "name": extract_name(text),
        "father_name": extract_father_name(text),
        "dob": extract_dob(text),
        "dob": dob,
        "issue": issue,
        "expiry": expiry,
        "raw_text": text
    }

def normalize_address(text):
    text = text.replace("ء", "")
    text = re.sub(r"\s+", " ", text)
    return text.strip(" ,۔")

def extract_cnic_address(text):

    lines = [normalize_address(l) for l in text.split("\n") if l.strip()]

    include_keywords = [
        "ضلع",
        "تحصیل",
        "ڈاک",
        "ڈاکخانہ",
        "گاؤں",
        "موضع",
        "چک",

    ]

    ignore_patterns = [
        r"\d{5}-\d{7}-\d",
        r"^\d+$",
        "Pakistan",
        "Registrar",
        "گمشده",
        "~",
    ]

    picked = []

    for line in lines:
        if any(re.search(p, line, re.IGNORECASE) for p in ignore_patterns):
            continue

        if any(k in line for k in include_keywords):
            picked.append(line)

    # remove duplicates while preserving order
    seen = set()
    cleaned = []
    for p in picked:
        if p not in seen:
            seen.add(p)
            cleaned.append(p)

    # join into single address string
    return "، ".join(cleaned)





def check_expiry(expiry_date_text):

    try:
        expiry_date = expiry_date_text.replace(" ", "")  # remove ALL spaces
        expiry = datetime.strptime(expiry_date, "%d.%m.%Y").date()
        today = datetime.today().date()

        return {
            "is_expired": expiry < today,
            "expiring_within_60_days": today <= expiry <= today + timedelta(days=60)
        }

    except Exception:
        return {
            "is_expired": None,
            "expiring_within_60_days": None
        }


def similarity(a, b):
    return fuzz.ratio(a.lower(), b.lower())