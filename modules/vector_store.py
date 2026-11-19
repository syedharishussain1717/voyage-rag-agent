
from pathlib import Path
from functools import lru_cache

import chromadb

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


# Project directories
BASE_DIR = Path(__file__).resolve().parent.parent
CHROMA_PATH = BASE_DIR / "chroma_db"

COLLECTION_NAME = "voyage_collection"

# Local embedding model
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


@lru_cache(maxsize=1)
def get_embeddings():
    """
    Load the Hugging Face embedding model once.
    """

    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )


def create_vector_store(chunks):
    """
    Create or rebuild the ChromaDB collection
    using the supplied PDF document chunks.
    """

    if not chunks:
        raise ValueError("No document chunks were provided.")

    CHROMA_PATH.mkdir(parents=True, exist_ok=True)

    # Connect to persistent ChromaDB
    client = chromadb.PersistentClient(
        path=str(CHROMA_PATH)
    )

    # Remove the previous collection to prevent duplicate indexing
    existing_collections = [
        collection.name
        for collection in client.list_collections()
    ]

    if COLLECTION_NAME in existing_collections:
        client.delete_collection(
            name=COLLECTION_NAME
        )

    # Generate embeddings and store document chunks
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=get_embeddings(),
        collection_name=COLLECTION_NAME,
        persist_directory=str(CHROMA_PATH)
    )

    print(f"Successfully indexed {len(chunks)} chunks.")

    return vector_store


def load_vector_store():
    """
    Load the previously created persistent ChromaDB collection.
    """

    if not CHROMA_PATH.exists():
        raise FileNotFoundError(
            "Vector database not found. Please upload and index a PDF first."
        )

    client = chromadb.PersistentClient(
        path=str(CHROMA_PATH)
    )

    try:
        collection = client.get_collection(
            name=COLLECTION_NAME
        )
    except Exception as error:
        raise ValueError(
            "VoyageAI vector collection does not exist. "
            "Please index your PDF first."
        ) from error

    if collection.count() == 0:
        raise ValueError(
            "The vector database is empty. Please index your PDF again."
        )

    vector_store = Chroma(
        client=client,
        collection_name=COLLECTION_NAME,
        embedding_function=get_embeddings()
    )

    print(
        f"Loaded vector database with {collection.count()} chunks."
    )

    return vector_store
