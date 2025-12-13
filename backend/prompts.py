from typing import List, Literal
from dataclasses import dataclass

TutorMode = Literal["qa", "quiz", "explain_simple", "explain_analogy"]


@dataclass
class RetrievedChunk:
    content: str
    source_id: str
    score: float


SYSTEM_TUTOR = """You are an AI study coach for the course "Introduction to Data Structures".
You answer questions STRICTLY based on the provided context.
If the answer is not in the context, say "I don't know from the provided materials."
Be concise but clear, and show which sources you used.
"""


def format_context(chunks: List[RetrievedChunk]) -> str:
    parts = []
    for idx, c in enumerate(chunks, start=1):
        parts.append(f"[Source {idx} | id={c.source_id} | score={c.score:.2f}]\n{c.content}\n")
    return "\n\n".join(parts)


def build_tutor_prompt(
    mode: TutorMode,
    question: str,
    chunks: List[RetrievedChunk],
) -> list:
    """
    Returns a list of messages (OpenAI chat format).
    """
    context_str = format_context(chunks)

    if mode == "qa":
        user_msg = f"""You are helping a student answer a question.

CONTEXT:
{context_str}

QUESTION:
{question}

INSTRUCTIONS:
- ONLY use the context.
- If you cannot find the answer, say you don't know from the provided materials.
- Cite sources like [Source 1], [Source 2] when relevant.
"""
    elif mode == "quiz":
        user_msg = f"""You are generating practice questions based on course notes.

CONTEXT:
{context_str}

TASK:
Generate 5 multiple-choice questions (MCQs) based ONLY on the context.
For each question, produce JSON with:
- question (string)
- options (array of 4 strings)
- correct_index (0-3)
- explanation (string)
- source (e.g. "Source 1")

Return a JSON array ONLY. No extra commentary.
"""
    elif mode == "explain_simple":
        user_msg = f"""You are explaining a concept to a beginner student.

CONTEXT:
{context_str}

QUESTION:
{question}

INSTRUCTIONS:
- Explain the answer like you're talking to a motivated 12-year-old.
- Use simple language and short sentences.
- Avoid jargon unless necessary and explain it when used.
- Only use the context. If you don't know, say so.
"""
    elif mode == "explain_analogy":
        user_msg = f"""You are explaining a concept using real-world analogies.

CONTEXT:
{context_str}

QUESTION:
{question}

INSTRUCTIONS:
- Provide a clear answer PLUS at least one concrete real-world analogy.
- Only use the context. If you don't know, say so.
"""
    else:
        raise ValueError(f"Unsupported mode: {mode}")

    messages = [
        {"role": "system", "content": SYSTEM_TUTOR},
        {"role": "user", "content": user_msg},
    ]
    return messages
