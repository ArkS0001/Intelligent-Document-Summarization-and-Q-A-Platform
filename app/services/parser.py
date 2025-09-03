import docx2txt
from PyPDF2 import PdfReader

def parse_file(file_path: str) -> str:
    if file_path.endswith(".pdf"):
        reader = PdfReader(file_path)
        text = "".join([page.extract_text() for page in reader.pages if page.extract_text()])
    elif file_path.endswith(".docx"):
        text = docx2txt.process(file_path)
    else:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
    return text
