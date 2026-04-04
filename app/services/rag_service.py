from pathlib import Path
import json
import numpy as np
import pandas as pd
import faiss
from openai import OpenAI

from app.core.config import settings


BASE_DIR = Path(__file__).resolve().parent.parent.parent
RAG_DIR = BASE_DIR / "rag_store"
RAG_DIR.mkdir(parents=True, exist_ok=True)

INDEX_PATH = RAG_DIR / "faiss.index"
METADATA_PATH = RAG_DIR / "chunks.json"

EMBEDDING_MODEL = "text-embedding-3-small"
LLM_MODEL = "gpt-4.1-mini"


def get_openai_client() -> OpenAI:
    if not settings.openai_api_key:
        raise ValueError("OPENAI_API_KEY is missing in .env")
    return OpenAI(api_key=settings.openai_api_key)


def dataframe_to_chunks(df: pd.DataFrame) -> list[str]:
    chunks = []

    for idx, row in df.iterrows():
        row_text = " | ".join([f"{col}: {row[col]}" for col in df.columns])
        chunks.append(f"Row {idx + 1}: {row_text}")

    return chunks


def create_embeddings(texts: list[str]) -> np.ndarray:
    client = get_openai_client()

    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=texts
    )

    vectors = [item.embedding for item in response.data]
    return np.array(vectors, dtype="float32")


def save_faiss_index(vectors: np.ndarray):
    dimension = vectors.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(vectors)
    faiss.write_index(index, str(INDEX_PATH))


def save_metadata(chunks: list[str]):
    with open(METADATA_PATH, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)


def load_faiss_index():
    if not INDEX_PATH.exists():
        raise FileNotFoundError("FAISS index not found. Please run /rag/index first.")
    return faiss.read_index(str(INDEX_PATH))


def load_metadata() -> list[str]:
    if not METADATA_PATH.exists():
        raise FileNotFoundError("Chunk metadata not found. Please run /rag/index first.")
    with open(METADATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def build_rag_index_from_dataframe(df: pd.DataFrame) -> dict:
    chunks = dataframe_to_chunks(df)
    vectors = create_embeddings(chunks)

    save_faiss_index(vectors)
    save_metadata(chunks)

    return {
        "message": "RAG index created successfully",
        "chunks_indexed": len(chunks),
        "embedding_model": EMBEDDING_MODEL
    }


def retrieve_relevant_chunks(question: str, top_k: int = 3) -> list[str]:
    client = get_openai_client()

    question_embedding_response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=[question]
    )

    question_vector = np.array(
        [question_embedding_response.data[0].embedding],
        dtype="float32"
    )

    index = load_faiss_index()
    chunks = load_metadata()

    distances, indices = index.search(question_vector, top_k)

    results = []
    for idx in indices[0]:
        if idx != -1 and idx < len(chunks):
            results.append(chunks[idx])

    return results


def ask_rag(question: str, top_k: int = 3) -> dict:
    client = get_openai_client()

    retrieved_chunks = retrieve_relevant_chunks(question, top_k=top_k)
    context = "\n".join(retrieved_chunks)

    prompt = f"""
You are a helpful data assistant.

Answer the user's question only using the retrieved dataset rows below.
If the answer is not clearly supported by the retrieved rows, say that the available retrieved context is insufficient.

Retrieved rows:
{context}

User question:
{question}
"""

    response = client.responses.create(
        model=LLM_MODEL,
        input=prompt
    )

    return {
        "answer": response.output_text,
        "retrieved_chunks": retrieved_chunks,
        "source": "RAG + dataset"
    }