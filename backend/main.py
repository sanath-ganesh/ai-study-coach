from fastapi import FastAPI
from pydantic import BaseModel
from typing import Literal, List

from .rag_pipeline import rag_answer
from .synthetic_data import generate_synthetic_questions


class AskRequest(BaseModel):
    question: str
    mode: Literal["qa", "quiz", "explain_simple", "explain_analogy"] = "qa"


class AskResponse(BaseModel):
    answer: str
    used_sources: List[str]


class SyntheticRequest(BaseModel):
    course_name: str
    max_chunks: int = 20


class SyntheticResponse(BaseModel):
    file_path: str


app = FastAPI(title="AI Study Coach API")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ask", response_model=AskResponse)
def ask(req: AskRequest):
    answer, chunks = rag_answer(req.question, req.mode)
    sources = [c.source_id for c in chunks]
    return AskResponse(answer=answer, used_sources=sources)


@app.post("/generate_synthetic", response_model=SyntheticResponse)
def generate_synthetic(req: SyntheticRequest):
    path = generate_synthetic_questions(req.course_name, req.max_chunks)
    return SyntheticResponse(file_path=str(path))
