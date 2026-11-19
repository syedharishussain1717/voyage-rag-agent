
from modules.pdf_loader import load_and_split_pdf

pdf_path = "temp/VoyageAI Official Destination Guide Japan (Tokyo & Kyoto).pdf"

chunks = load_and_split_pdf(pdf_path)

print("PDF loaded successfully!")
print("Total chunks:", len(chunks))

print("\nFirst chunk:")
print(chunks[0].page_content[:500])

print("\nMetadata:")
print(chunks[0].metadata)
