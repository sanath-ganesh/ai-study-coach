from backend.chunking import clean_text, chunk_text


def test_clean_text_basic():
    raw = "Hello   world\n\nThis\tis   a test."
    cleaned = clean_text(raw)
    assert "  " not in cleaned
    assert cleaned.startswith("Hello")
    assert cleaned.endswith("test.")


def test_chunk_text_overlap():
    text = " ".join(["word"] * 3000)  # 3000 words
    chunks = chunk_text(text, chunk_size=500, overlap=100)
    assert len(chunks) > 1
    # Check overlap: the end of chunk 0 and start of chunk 1 should share some words
    first_chunk_words = chunks[0].split()
    second_chunk_words = chunks[1].split()
    overlap_count = len(set(first_chunk_words[-100:]).intersection(second_chunk_words[:100]))
    assert overlap_count > 0
