import io
import pypdf
from PIL import Image
import pytesseract
import streamlit as st

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract text from all pages of a PDF via pypdf."""
    reader = pypdf.PdfReader(io.BytesIO(file_bytes))
    pages = [page.extract_text() or "" for page in reader.pages]
    return "\n".join(pages).strip()


def extract_text_from_image(file_bytes: bytes) -> str:
    """OCR an image file via pytesseract."""
    img = Image.open(io.BytesIO(file_bytes))
    return pytesseract.image_to_string(img).strip()


def extract_text(uploaded_file) -> str:
    """Dispatch to the correct extractor based on file type."""
    raw = uploaded_file.read()
    name = uploaded_file.name.lower()
    if name.endswith(".pdf"):
        text = extract_text_from_pdf(raw)
    elif name.endswith((".png", ".jpg", ".jpeg", ".webp", ".tiff", ".bmp")):
        text = extract_text_from_image(raw)
    else:
        text = raw.decode("utf-8", errors="ignore").strip()
    
    # Truncate to prevent Groq 413 "Request Entity Too Large" limits
    max_chars = 15000
    if len(text) > max_chars:
        st.warning(f"⚠️ Document is very large ({len(text)} characters). Truncating to first {max_chars} characters for analysis.")
        return text[:max_chars]
    return text
