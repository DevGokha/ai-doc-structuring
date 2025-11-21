import pdfplumber

def extract_lines_from_pdf(pdf_path: str):
    lines = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            for line in text.split("\n"):
                line = line.strip()
                if line:
                    lines.append({
                        "page": page_num,
                        "line_text": line
                    })
    return lines

def extract_full_text(pdf_path: str) -> str:
    """Return the full text of the PDF as one string."""
    texts = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            t = page.extract_text() or ""
            texts.append(t)
    return "\n".join(texts)
