import os

DOCS_DIR = "docs"

def load_docs():
    docs = {}
    for filename in os.listdir(DOCS_DIR):
        if filename.endswith(".txt"):
            path = os.path.join(DOCS_DIR, filename)
            with open(path, "r", encoding="utf-8") as f:
                docs[filename] = f.read()
    return docs

if __name__ == "__main__":
    docs = load_docs()
    for filename, content in docs.items():
        print(f"{filename}: {len(content)} chars")

def chunk_text(text):
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    return paragraphs

print(chunk_text(docs["Test Note 1.txt"]))

print(chunk_text(docs["Test Note 3.txt"]))