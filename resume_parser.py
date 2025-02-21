import io
import docx2txt
from pypdf import PdfReader

def extract_text(uploaded_file):
    """Extract text from PDF or DOCX file."""
    file_bytes = uploaded_file.read()
    if uploaded_file.name.lower().endswith(".pdf"):
        pdf_reader = PdfReader(io.BytesIO(file_bytes))
        text = "\n".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])
    elif uploaded_file.name.lower().endswith(".docx"):
        text = docx2txt.process(io.BytesIO(file_bytes))
    else:
        text = ""
    return text.strip()
