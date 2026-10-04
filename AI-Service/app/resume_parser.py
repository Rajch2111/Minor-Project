"""
Resume Parser — extracts text from PDF/DOCX and structured fields
"""
import re
from io import BytesIO

from pypdf import PdfReader
from docx import Document

SKILL_KEYWORDS = [
    "python", "java", "c++", "c", "javascript", "react", "node.js", "node",
    "mongodb", "sql", "express", "django", "flask", "machine learning",
    "deep learning", "nlp", "aws", "docker", "kubernetes", "redis",
    "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch", "git",
    "html", "css", "tailwind", "rest api", "linux", "spring boot",
]

EDUCATION_KEYWORDS = ["b.tech", "btech", "b.e", "m.tech", "mtech", "bachelor", "master", "phd", "diploma"]
SECTION_HEADERS = ["education", "skills", "experience", "projects", "certifications", "achievements"]


def extract_text_from_pdf(file_bytes: bytes) -> str:
    reader = PdfReader(BytesIO(file_bytes))
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def extract_text_from_docx(file_bytes: bytes) -> str:
    doc = Document(BytesIO(file_bytes))
    return "\n".join(p.text for p in doc.paragraphs)


def extract_text(filename: str, file_bytes: bytes) -> str:
    name = filename.lower()
    if name.endswith(".pdf"):
        return extract_text_from_pdf(file_bytes)
    if name.endswith(".docx"):
        return extract_text_from_docx(file_bytes)
    if name.endswith(".txt"):
        return file_bytes.decode("utf-8", errors="ignore")
    raise ValueError("Unsupported file type. Use PDF, DOCX or TXT.")


def extract_email(text: str):
    match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", text)
    return match.group(0) if match else None


def extract_phone(text: str):
    match = re.search(r"(\+?\d[\d\s-]{8,}\d)", text)
    return match.group(0).strip() if match else None


def extract_skills(text: str):
    lowered = text.lower()
    return sorted({s for s in SKILL_KEYWORDS if s in lowered})


def extract_sections(text: str):
    lowered = text.lower()
    return [h for h in SECTION_HEADERS if h in lowered]


def extract_education(text: str):
    lowered = text.lower()
    return [e for e in EDUCATION_KEYWORDS if e in lowered]


def parse_resume(filename: str, file_bytes: bytes) -> dict:
    text = extract_text(filename, file_bytes)
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    name_guess = lines[0] if lines else None

    return {
        "name_guess": name_guess,
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text),
        "education_found": extract_education(text),
        "sections_found": extract_sections(text),
        "raw_text_length": len(text),
    }
