import os
import ollama
import chromadb

# Constants
DOCS_DIR = "docs"

# Initialize ChromaDB client and collection
client = chromadb.PersistentClient(path="db")
collection = client.get_or_create_collection("docs")

# Retrieve documents from the docs directory
def load_docs():
    docs = {}
    for filename in os.listdir(DOCS_DIR):
        if filename.endswith(".txt"):
            path = os.path.join(DOCS_DIR, filename)
            with open(path, "r", encoding="utf-8") as f:
                docs[filename] = f.read()
    return docs

# Chunk text into paragraphs
def chunk_text(text):
    return[text.strip()]

# Embed text using the Ollama embeddings model
def embed(text):
    response = ollama.embeddings(model="nomic-embed-text", prompt=text)
    return response["embedding"]

# Ingest documents into the database
def ingest():
    docs = load_docs()
    chunk_id = 0
    for filename, content in docs.items():
        chunks = chunk_text(content)
        for chunk in chunks:
            collection.add(
                ids=[str(chunk_id)],
                embeddings=[embed(chunk)],
                documents=[chunk],
                metadatas=[{"filename": filename}],
            )
            chunk_id += 1
        print(f"Ingested {chunk_id} chunks from {len(docs)} docs.")

if __name__ == "__main__":
    ingest()
