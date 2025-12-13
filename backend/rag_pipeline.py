from typing import List, Tuple
from pathlib import Path
import chromadb
from chromadb.config import Settings
from openai import OpenAI

from .config import VECTOR_DB_DIR, CHAT_MODEL, TOP_K, MIN_SIMILARITY_SCORE
from .embeddings import embed_text
from .prompts import build_tutor_prompt, RetrievedChunk, TutorMode
from .config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


def get_chroma_client():
    VECTOR_DB_DIR.mkdir(parents=True, exist_ok=True)
    client = chromadb.Client(
        Settings(
            persist_directory=str(VECTOR_DB_DIR),
            is_persistent=True,
        )
    )
    return client


def get_collection(name: str = "course_rag"):
    client = get_chroma_client()
    return client.get_or_create_collection(name=name)


def ingest_chunks_from_file(processed_file: Path, course_name: str):
    """
    Reads the processed chunks file and stores each chunk in Chroma.
    """
    collection = get_collection()
    docs = []
    metadatas = []
    ids = []

    with open(processed_file, "r", encoding="utf-8") as f:
        current_chunk_lines = []
        chunk_index = 0
        for line in f:
            if line.startswith("---chunk-"):
                if current_chunk_lines:
                    content = " ".join(current_chunk_lines).strip()
                    if content:
                        doc_id = f"{course_name}_{processed_file.stem}_chunk_{chunk_index}"
                        docs.append(content)
                        metadatas.append({
                            "course": course_name,
                            "source_file": processed_file.name,
                            "chunk_index": chunk_index,
                        })
                        ids.append(doc_id)
                        chunk_index += 1
                    current_chunk_lines = []
            else:
                current_chunk_lines.append(line.strip())

        # Last chunk
        if current_chunk_lines:
            content = " ".join(current_chunk_lines).strip()
            if content:
                doc_id = f"{course_name}_{processed_file.stem}_chunk_{chunk_index}"
                docs.append(content)
                metadatas.append({
                    "course": course_name,
                    "source_file": processed_file.name,
                    "chunk_index": chunk_index,
                })
                ids.append(doc_id)

    # Embed and add to Chroma
    embeddings = [embed_text(d) for d in docs]
    collection.add(
        ids=ids,
        documents=docs,
        metadatas=metadatas,
        embeddings=embeddings,
    )


def retrieve_relevant_chunks(
    query: str,
    top_k: int = TOP_K,
) -> List[RetrievedChunk]:
    collection = get_collection()
    query_embedding = embed_text(query)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    docs = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]  # smaller is closer

    # Convert distance to a crude "similarity" (here 1 / (1 + distance))
    chunks: List[RetrievedChunk] = []
    for doc, meta, dist in zip(docs, metadatas, distances):
        similarity = 1 / (1 + dist)
        if similarity < MIN_SIMILARITY_SCORE:
            continue
        source_id = f"{meta.get('source_file')}#{meta.get('chunk_index')}"
        chunks.append(RetrievedChunk(content=doc, source_id=source_id, score=similarity))

    return chunks


def call_llm(messages: list) -> str:
    """
    Call OpenAI chat model.
    """
    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=messages,
        temperature=0.2,
    )
    return response.choices[0].message.content


def rag_answer(
    question: str,
    mode: TutorMode = "qa",
) -> Tuple[str, List[RetrievedChunk]]:
    """
    Main RAG flow: retrieve -> build prompt -> call LLM.
    """
    chunks = retrieve_relevant_chunks(question)
    if not chunks:
        # No good context found; still call LLM but with empty context & ask it to say I don't know.
        chunks = []

    messages = build_tutor_prompt(mode=mode, question=question, chunks=chunks)
    answer = call_llm(messages)
    return answer, chunks
