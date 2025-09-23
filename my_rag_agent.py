from typing import List, Dict
from embedding_store import query_collection
import os
import google.generativeai as genai
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file


class RAGAgent:
    def __init__(self, use_llm: bool = False, similarity_threshold: float = 0.6):
        """
        RAGAgent for retrieval + optional Gemini synthesis.
        - use_llm: if True, prepend a synthesized Gemini answer
        - similarity_threshold: only consider chunks with distance less than this
        """
        print(f"Initializing RAGAgent(use_llm={use_llm}, similarity_threshold={similarity_threshold})")
        self.use_llm = use_llm
        self.similarity_threshold = similarity_threshold

        # Configure Gemini once if synthesis is enabled
        if self.use_llm:
            api_key = os.getenv("GOOGLE_API_KEY")   # <-- using .env variable
            if not api_key:
                raise ValueError("GOOGLE_API_KEY environment variable is not set.")
            genai.configure(api_key=api_key)
            self.llm = genai.GenerativeModel("gemini-1.5-flash")  # free Gemini model
        else:
            self.llm = None

    def retrieve(self, query: str, top_k: int = 10) -> List[Dict]:
        """Retrieve top-k chunks from the vector store."""
        candidates = query_collection(query, top_k=top_k)
        filtered = [c for c in candidates if c.get("distance", 1.0) <= self.similarity_threshold]
        return filtered
 
    def answer(self, query: str, top_k: int = 10, n_best: int = 3) -> List[Dict]:
        candidates = sorted(
            self.retrieve(query, top_k=top_k),
            key=lambda x: x.get("distance", 1.0)
        )

        if not candidates:
            return [{"answer": "No relevant documents found.", "source": None, "reason": None, "distance": None}]

        results = []
        seen_texts = set()

        # 🔹 Split each candidate into smaller sub-chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=300,   # characters per sub-chunk
            chunk_overlap=50
        )

        for c in candidates:
            # Split candidate text
            chunks = text_splitter.split_text(c["document"].strip())
            source = c["metadata"].get("source", "unknown")
            parent_index = c["metadata"].get("chunk_index", -1)
            distance = c.get("distance", None)

            for i, chunk_text in enumerate(chunks):
                chunk_text = chunk_text.strip()
                if chunk_text in seen_texts:
                    continue
                seen_texts.add(chunk_text)

                reason = f"Retrieved from chunk {parent_index}.{i} in {source} (distance={distance:.4f})."
                results.append({
                    "answer": chunk_text,
                    "source": source,
                    "reason": reason,
                    "distance": distance
                })

                if len(results) >= n_best:
                    break
            if len(results) >= n_best:
                break

        # Pad if not enough results
        while len(results) < n_best:
            results.append({
                "answer": "No more relevant answers found.",
                "source": None,
                "reason": None,
                "distance": None
            })

        # 🔹 Optional LLM synthesis at top
        if getattr(self, "use_llm", False) and hasattr(self, "llm") and results:
            context = " ".join([r["answer"] for r in results if r["answer"] != "No more relevant answers found."])
            prompt = f"Answer the question based only on this context:\n{context}\n\nQ: {query}\nA:"
            response = self.llm.generate_content(prompt)
            llm_answer = response.text if hasattr(response, "text") else str(response)

            results.insert(0, {
                "answer": llm_answer,
                "source": "Synthesized from retrieved docs",
                "reason": "Generated using Gemini (gemini-1.5-flash)",
                "distance": None
            })

        return results[:n_best] if not getattr(self, "use_llm", False) else results[:n_best+1]


        
 