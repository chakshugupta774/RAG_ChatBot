# RAGChatbot


A Retrieval-Augmented Generation (RAG) Chatbot that allows users to query uploaded documents (PDF, DOCX, TXT, CSV, PPTX, XLSX) and get accurate answers with context. The chatbot leverages **vector embeddings** for retrieval and optionally uses **Google Gemini LLM** for synthesized responses.

---

## Features

- 📄 Upload multiple documents for indexing.
- 🧠 Retrieve relevant chunks using semantic similarity.
- 🤖 Optional Google Gemini synthesis for generating context-aware answers.
- ⚡ Graceful handling of Gemini quota limits; always returns retrieved answers even if LLM fails.
- 🎯 Shows similarity score and source document for each response.
- 💻 Simple Streamlit interface for interactive Q&A.

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/chakshugupta774/RAGChatbot.git
cd RAGChatbot
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file and add your **Google Gemini API key**:

```env
GEN_API_KEY=your_google_gemini_api_key
```

---

## Usage

Run the Streamlit app:

```bash
streamlit run app.py
```

1. Open the app in your browser.
2. Upload your documents (PDF, DOCX, TXT, CSV, PPTX, XLSX).
3. Configure Top-k retrieval, Number of answers, Similarity threshold, and optionally enable Gemini synthesis.
4. Enter your query and get responses with source and similarity score.

---

## Code Structure

```
RAGChatbot/
│
├── app.py                 # Streamlit app
├── my_rag_agent.py        # RAG Agent with optional Gemini integration
├── embedding_store.py     # Chroma vector store + embeddings
├── document_loader.py     # Utility for reading uploaded files
├── requirements.txt       # Python dependencies
└── README.md

```


## How it Works

1. Document Indexing: Uploaded documents are split into meaningful chunks and embedded using sentence-transformers/all-MiniLM-L6-v2.
2. Vector Store: Chunks are stored in a persistent ChromaDB vector store.
3. Query: User question is embedded and matched with the top-k most similar chunks.
4. Optional LLM: Gemini LLM synthesizes a final answer based on the retrieved chunks.
5. Output: Returns answers along with source document and similarity score.


## Notes

1. Free-tier Gemini quota: 50 requests/day. Quota resets at 00:00 UTC (05:30 AM IST).
2. If quota is exceeded, only retrieved answers from the vector store will be shown.
3. Supports documents in multiple formats for flexible Q&A.


## Acknowledgements

- [Google Gemini](https://developers.generativeai.google) for LLM synthesis.
- [ChromaDB](https://www.trychroma.com/) for vector database.
- [Sentence Transformers](https://www.sbert.net/) for embeddings.
- [Streamlit](https://streamlit.io/) for interactive UI.
