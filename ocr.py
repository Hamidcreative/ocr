from pdf2image import convert_from_path
import easyocr

# reader = easyocr.Reader(['en'])
reader = easyocr.Reader(['en', 'ur'], gpu=False)
def extract_text_from_pdf(path):
    import pdfplumber
    pages = convert_from_path(path)
    text = ""

    for page in pages:
        temp_file = "temp_page.jpg"
        page.save(temp_file, "JPEG")

        result = reader.readtext(temp_file)

        text += "\n".join([item[1] for item in result])
        text += "\n"

    return text

def extract_text_from_image(path):
    result = reader.readtext(path)

    text = "\n".join([item[1] for item in result])
    return text

def extract_text(path):

    if path.lower().endswith(".pdf"):
        text = extract_text_from_pdf(path)
    else:
        text = extract_text_from_image(path)

    return text







