import streamlit as st
from document_loader import load_document
from embedding_store import chunk_text, embed_and_store
from my_rag_agent import RAGAgent

st.title("🧠 RAG Chatbot")

# File uploader
uploaded_files = st.file_uploader(
    "Upload documents",
    type=["pdf", "docx", "txt", "csv", "xlsx", "pptx"],
    accept_multiple_files=True
)

# Sidebar controls
st.sidebar.header("⚙ Settings")
top_k = st.sidebar.number_input("Top-k retrieval", min_value=1, max_value=20, value=5, step=1)
n_best = st.sidebar.number_input("Number of answers per query", min_value=1, max_value=10, value=3, step=1)
similarity_threshold = st.sidebar.slider("Similarity threshold", 0.0, 1.0, 0.6, 0.05)
use_llm = st.sidebar.checkbox("Use Gemini synthesis (gemini-1.5-flash)", value=False)

# Index uploaded documents
if uploaded_files:
    st.subheader("Indexing Documents...")
    for file in uploaded_files:
        docs = load_document(file.name, file.read())
        for doc in docs:
            chunks = chunk_text(doc["text"])
            embed_and_store(chunks, source=doc["source"])
    st.success(f"Indexed {len(uploaded_files)} documents.")

# Initialize RAG agent
agent = RAGAgent(use_llm=use_llm, similarity_threshold=similarity_threshold)

# User query
query = st.text_input("Enter your question:")

if query:
    responses = agent.answer(query, top_k=top_k, n_best=n_best)

    # Display responses
    st.subheader("🤖 Responses")
    for i, r in enumerate(responses, 1):
        st.markdown(f"### Response {i}")
        st.write(r["answer"])
        st.caption(f"Source: {r['source'] or 'Unknown'} | Similarity Score: {r.get('score', 'N/A')}")
        st.markdown("---")

