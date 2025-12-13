import json
from pathlib import Path
from typing import List
from openai import OpenAI

from .config import SYNTHETIC_DATA_DIR, CHAT_MODEL, OPENAI_API_KEY
from .rag_pipeline import get_collection

client = OpenAI(api_key=OPENAI_API_KEY)


def generate_synthetic_questions(course_name: str, max_chunks: int = 20) -> Path:
    """
    Generate synthetic Q&A pairs for evaluation/practice.
    Pulls random-ish documents from the vector store and asks the LLM to create questions.
    """
    SYNTHETIC_DATA_DIR.mkdir(parents=True, exist_ok=True)
    collection = get_collection()

    # Get all documents metadata
    # Chroma doesn't have "list all" in a trivial way, but we can get them via get()
    # For simplicity, we assume collection has up to a few thousand docs and we fetch them all.
    all_ids = collection.get().get("ids", [])
    all_docs = collection.get().get("documents", [])
    all_meta = collection.get().get("metadatas", [])

    # use only the first max_chunks docs for demo
    selected = list(zip(all_ids, all_docs, all_meta))[:max_chunks]

    synthetic_entries = []

    for doc_id, doc, meta in selected:
        prompt = f"""You are an exam question writer.

CONTEXT:
{doc}

TASK:
Generate 3 exam-style questions and detailed answers based ONLY on the context.

Return JSON with:
[
  {{
    "question": "...",
    "answer": "...",
    "difficulty": "easy|medium|hard"
  }},
  ...
]
"""

        response = client.chat.completions.create(
            model=CHAT_MODEL,
            messages=[
                {"role": "system", "content": "You generate exam questions and answers strictly from provided context."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
        )

        content = response.choices[0].message.content
        # Try to parse JSON; if it fails, skip this doc
        try:
            data = json.loads(content)
            for item in data:
                item["source_id"] = doc_id
                item["course"] = course_name
                synthetic_entries.append(item)
        except Exception:
            # In a real system you'd log this
            continue

    output_path = SYNTHETIC_DATA_DIR / f"{course_name}_synthetic_qa.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(synthetic_entries, f, indent=2, ensure_ascii=False)

    return output_path
