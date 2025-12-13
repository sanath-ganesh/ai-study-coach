from typing import List
from pathlib import Path
from pypdf import PdfReader
import re
from .config import CHUNK_SIZE, CHUNK_OVERLAP, PROCESSED_DATA_DIR


def load_pdf_text(pdf_path: Path) -> str:
    """
    Extracts text from a PDF file.
    """
    reader = PdfReader(str(pdf_path))
    pages = [page.extract_text() or "" for page in reader.pages]
    return "\n\n".join(pages)


def clean_text(text: str) -> str:
    """
    Basic cleanup: normalize whitespace, remove weird characters.
    """
    text = text.replace("\r", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> List[str]:
    """
    Simple sliding-window chunking over text.
    """
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks


def process_pdf(pdf_path: Path, course_name: str) -> Path:
    """
    Loads, cleans, and chunks PDF; saves chunks as a .txt file with separators.
    Returns path to processed file.
    """
    text = load_pdf_text(pdf_path)
    text = clean_text(text)
    chunks = chunk_text(text)

    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    output_path = PROCESSED_DATA_DIR / f"{course_name}_{pdf_path.stem}_chunks.txt"

    with open(output_path, "w", encoding="utf-8") as f:
        for i, chunk in enumerate(chunks):
            f.write(f"---chunk-{i}---\n")
            f.write(chunk + "\n")

    return output_path
