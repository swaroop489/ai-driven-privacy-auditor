import re

def clean_ocr_text(text: str) -> str:
    text = text.replace("\n", " ")
    text = re.sub(r"[^A-Za-z0-9@.\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()
