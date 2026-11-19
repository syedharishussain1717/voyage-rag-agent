
from modules.pdf_loader import load_and_split_pdf
from modules.vector_store import (
    create_vector_store,
    load_vector_store
)

PDF_PATH = (
    "temp/VoyageAI Official Destination Guide Japan (Tokyo & Kyoto).pdf"
)

print("Step 1: Loading PDF...")

chunks = load_and_split_pdf(PDF_PATH)

print("Extracted chunks:", len(chunks))

print("\nStep 2: Creating ChromaDB vector store...")

vector_store = create_vector_store(chunks)

print("\nStep 3: Testing document retrieval...")

query = "What is the emergency telephone number for police in Japan?"

results = vector_store.similarity_search(
    query,
    k=3
)

for index, document in enumerate(results, start=1):
    print(f"\nResult {index}")
    print("Page:", document.metadata.get("page_number"))
    print("Content:")
    print(document.page_content[:400])

print("\nStep 4: Testing persistent database loading...")

loaded_store = load_vector_store()

print("\nStep 5: Testing retrieval after loading...")

loaded_results = loaded_store.similarity_search(
    query,
    k=3
)

print("Retrieved documents:", len(loaded_results))

print("\nSUCCESS: Vector database tests completed!")
