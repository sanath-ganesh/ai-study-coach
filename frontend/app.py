import requests
import streamlit as st

API_URL = "http://localhost:8000"  # change if you deploy elsewhere

st.set_page_config(page_title="AI Study Coach", page_icon="", layout="wide")

st.title("AI Study Coach – Introduction to Data Structures")

st.markdown("""
Ask questions about your course materials, generate quizzes, or get simple explanations.

> Make sure you've run the ingestion script to load PDFs into the knowledge base.
""")

with st.sidebar:
    st.header("Mode")
    mode = st.radio(
        "Select interaction mode",
        options=[
            "Question Answering",
            "Explain Simply",
            "Explain with Analogy",
            "Generate Quiz Questions",
        ],
    )

    if st.button("Check API health"):
        try:
            r = requests.get(f"{API_URL}/health", timeout=5)
            st.success(f"API status: {r.json().get('status')}")
        except Exception as e:
            st.error(f"Error: {e}")


mode_map = {
    "Question Answering": "qa",
    "Explain Simply": "explain_simple",
    "Explain with Analogy": "explain_analogy",
    "Generate Quiz Questions": "quiz",
}

user_question = st.text_area("Your question or topic", height=120, placeholder="E.g., Explain how a binary search tree works.")

if st.button("Ask"):
    if not user_question.strip():
        st.warning("Please enter a question first.")
    else:
        with st.spinner("Thinking..."):
            try:
                payload = {
                    "question": user_question,
                    "mode": mode_map[mode],
                }
                r = requests.post(f"{API_URL}/ask", json=payload, timeout=60)
                r.raise_for_status()
                data = r.json()
                st.subheader("Answer")
                st.write(data["answer"])

                if data["used_sources"]:
                    st.subheader("Sources used")
                    st.write(", ".join(data["used_sources"]))
                else:
                    st.info("No strong matching sources were found (or retrieval threshold not met).")
            except Exception as e:
                st.error(f"Error: {e}")
