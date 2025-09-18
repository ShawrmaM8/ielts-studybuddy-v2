import fitz  # PyMuPDF

def extract_pdf(pdf_bytes):
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        if len(text.strip()) < 50:
            raise ValueError("PDF too short or unreadable—check format.")
        return text
    except Exception as e:
        raise ValueError(f"PDF extraction failed: {str(e)}")