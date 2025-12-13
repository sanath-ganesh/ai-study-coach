from backend.rag_pipeline import retrieve_relevant_chunks


def test_retrieve_empty_db():
    # If collection is empty, this should return an empty list, not crash
    chunks = retrieve_relevant_chunks("What is a linked list?")
    assert isinstance(chunks, list)
