# AI Study Coach

A generative AI project that uses Retrieval-Augmented Generation (RAG), prompt engineering, and synthetic data generation to help students study **Introduction to Data Structures** (or any course you configure).

## Features

- Question answering over your uploaded course materials
- Simple explanations and analogy-based explanations
- Automatic quiz generation (MCQs) from your notes
- Synthetic Q&A dataset generation for evaluation

## Tech Stack

- **Backend**: FastAPI, OpenAI API, ChromaDB
- **Frontend**: Streamlit
- **RAG**: Custom chunking + OpenAI embeddings + Chroma
- **Synthetic Data**: OpenAI chat model with constrained JSON prompts

## Setup

1. Clone the repo and install dependencies:

```bash
pip install -r requirements.txt
````

2. Set your OpenAI API key in environment or `.env`:

```bash
export OPENAI_API_KEY="sk-..."
```

3. Add course PDFs to `data/raw/`.

4. Ingest documents:

```bash
python -m backend.ingest_docs --course "intro_data_structures"
```

5. Run backend:

```bash
uvicorn backend.main:app --reload
```

6. Run frontend:

```bash
streamlit run frontend/app.py
```

Then open the Streamlit URL, ask questions, and generate quizzes.

## Project Structure

(see description in the main report / documentation)

## Evaluation

See `docs/report.pdf` for:

* System architecture diagram
* Implementation details
* Performance metrics
* Challenges & solutions
* Future improvements
* Ethical considerations
