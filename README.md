# RAGChatbot



RAGChatbot is a **Retrieval-Augmented Generation (RAG)** chatbot that allows users to upload documents (PDF, DOCX, TXT, CSV, XLSX, PPTX) and ask questions. The chatbot retrieves relevant document chunks using embeddings and provides answers, optionally using **Google Gemini** for synthesis.

---

## Features

- Upload multiple document types: PDF, DOCX, TXT, CSV, XLSX, PPTX.
- Retrieve relevant document chunks using embeddings.
- Generate multiple distinct responses (`Answer 1`, `Answer 2`, etc.) from different chunks.
- Optional LLM synthesis using **Google Gemini API** for a concise, context-aware answer.
- Displays source and reasoning for each answer.
- Built with **Streamlit** for an interactive web interface.

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/RAGChatbot.git
cd RAGChatbot
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

> Required packages: `streamlit`, `google-generativeai`, `chromadb`, `sentence-transformers`, `python-dotenv`

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

1. Open the browser interface.
2. Upload your document(s).
3. Enter a question in the input box.
4. View multiple answers with sources, reasoning, and scores.

---

## Code Structure

```
RAGChatbot/
│
├─ app.py                # Streamlit interface
├─ rag_agent.py          # RAGAgent class (retrieval + answer logic)
├─ embedding_store.py    # Vector embedding and storage functions
├─ requirements.txt      # Project dependencies
└─ README.md
```

---

## Example

**Question:** `What are Azure networking services?`

**Answers:**

- **Answer 1:** `Azure Virtual Network, Load Balancer, VPN Gateway, and CDN provide secure, fast, and scalable networking.`\
  *Source: Microsoft Azure Overview\.txt | Chunk 1*

- **Answer 2:** `Azure Networking services include ExpressRoute, Azure DNS, and Traffic Manager for high availability and low latency.`\
  *Source: Microsoft Azure Overview\.txt | Chunk 2*

- **Answer 3:** `Azure Application Gateway and Front Door optimize traffic distribution and improve web app performance.`\
  *Source: Microsoft Azure Overview\.txt | Chunk 3*

> Optional synthesized answer using Google Gemini can appear at the top.

---

## Contributing

Contributions are welcome!

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/your-feature`.
3. Commit your changes: `git commit -m 'Add new feature'`.
4. Push to the branch: `git push origin feature/your-feature`.
5. Open a Pull Request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgements

- [Google Gemini](https://developers.generativeai.google) for LLM synthesis.
- [ChromaDB](https://www.trychroma.com/) for vector database.
- [Sentence Transformers](https://www.sbert.net/) for embeddings.
- [Streamlit](https://streamlit.io/) for interactive UI.

