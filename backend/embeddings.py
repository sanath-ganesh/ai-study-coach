from typing import List
from openai import OpenAI
from .config import OPENAI_API_KEY, EMBEDDING_MODEL

client = OpenAI(api_key=OPENAI_API_KEY)


def embed_texts(texts: List[str]) -> List[List[float]]:
    """
    Get embeddings for a list of texts from OpenAI.
    """
    if not texts:
        return []

    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=texts
    )

    return [item.embedding for item in response.data]


def embed_text(text: str) -> List[float]:
    """
    Convenience wrapper for a single text.
    """
    return embed_texts([text])[0]
