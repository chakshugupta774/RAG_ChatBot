import uuid
from typing import List
from transformers import AutoTokenizer
# from langchain_huggingface import HuggingFaceEmbeddings
from langchain.embeddings import HuggingFaceEmbeddings
import chromadb

CHROMA_DB_DIR = "chroma_vectorstore"
COLLECTION_NAME = "rag_collection"

# Embedding model
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

# Persistent ChromaDB client
client = chromadb.PersistentClient(path=CHROMA_DB_DIR)

# Chunking parameters
DEFAULT_CHUNK_SIZE = 1000   # bigger chunk
DEFAULT_CHUNK_OVERLAP = 50  # small overlap

def chunk_text(text: str, chunk_size: int = DEFAULT_CHUNK_SIZE, chunk_overlap: int = DEFAULT_CHUNK_OVERLAP) -> List[str]:
    """
    Splits text into meaningful chunks by sentences.
    """
    sentences = text.split(". ")
    chunks = []
    chunk = ""
    for sentence in sentences:
        if len(chunk + sentence) <= chunk_size:
            chunk += sentence + ". "
        else:
            chunks.append(chunk.strip())
            chunk = sentence + ". "
    if chunk:
        chunks.append(chunk.strip())
    return chunks

def embed_and_store(chunks: List[str], source: str = "unknown"):
    """
    Embeds chunks and stores them in ChromaDB.
    """
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"description": "Vector store for RAG chatbot"}
    )
    ids = [str(uuid.uuid4()) for _ in chunks]
    embeddings = embedding_model.embed_documents(chunks)
    collection.add(
        documents=chunks,
        ids=ids,
        metadatas=[{"source": source, "chunk_index": i, "text_length": len(chunks[i])} for i in range(len(chunks))],
        embeddings=embeddings
    )
    print(f"Stored {len(chunks)} chunks from {source} in ChromaDB")

def query_collection(query: str, top_k: int = 5):
    """
    Queries ChromaDB and returns top-k results.
    """
    if COLLECTION_NAME not in [col.name for col in client.list_collections()]:
        print("Collection not found!")
        return []

    collection = client.get_collection(name=COLLECTION_NAME)
    results = collection.query(query_texts=[query], n_results=top_k)
    output = []
    for i in range(len(results["ids"][0])):
        output.append({
            "id": results["ids"][0][i],
            "document": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            "distance": results["distances"][0][i]
        })
    return output
