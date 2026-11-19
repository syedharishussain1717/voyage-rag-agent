
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_and_split_pdf(
    pdf_path: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 200
):
    """
    Load a PDF and split it into smaller document chunks.

    Each chunk retains its original PDF page number
    so VoyageAI can provide accurate page citations.
    """

    file_path = Path(pdf_path)

    # Validate the PDF file
    if not file_path.exists():
        raise FileNotFoundError(
            f"PDF file not found: {file_path}"
        )

    if file_path.suffix.lower() != ".pdf":
        raise ValueError("Only PDF files are supported.")

    if chunk_size <= 0:
        raise ValueError("Chunk size must be greater than zero.")

    if chunk_overlap < 0 or chunk_overlap >= chunk_size:
        raise ValueError(
            "Chunk overlap must be non-negative "
            "and smaller than chunk size."
        )

    # Load PDF pages
    loader = PyPDFLoader(str(file_path))
    pages = loader.load()

    if not pages:
        raise ValueError("The uploaded PDF contains no readable pages.")

    # Preserve page metadata and use human-readable page numbers
    for page in pages:
        page_number = page.metadata.get("page", 0) + 1

        page.metadata["page_number"] = page_number
        page.metadata["source"] = file_path.name

    # Split documents into smaller chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        add_start_index=True
    )

    chunks = splitter.split_documents(pages)

    if not chunks:
        raise ValueError("No text chunks could be extracted from the PDF.")

    return chunks
