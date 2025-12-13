"""
Run this script to ingest PDFs from data/raw into the vector store.

Usage:
    python -m backend.ingest_docs --course "intro_data_structures"
"""

import argparse
from pathlib import Path
from .config import RAW_DATA_DIR
from .chunking import process_pdf
from .rag_pipeline import ingest_chunks_from_file


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--course", type=str, required=True, help="Course name label")
    args = parser.parse_args()

    pdf_files = list(RAW_DATA_DIR.glob("*.pdf"))
    if not pdf_files:
        print(f"No PDFs found in {RAW_DATA_DIR}. Put your notes there first.")
        return

    for pdf_path in pdf_files:
        print(f"Processing {pdf_path.name} ...")
        processed_file = process_pdf(pdf_path, args.course)
        print(f"Ingesting chunks from {processed_file.name} ...")
        ingest_chunks_from_file(processed_file, args.course)

    print("Done ingesting documents.")


if __name__ == "__main__":
    main()
