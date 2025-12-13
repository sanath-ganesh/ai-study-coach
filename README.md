# 📚 AI Study Coach

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
