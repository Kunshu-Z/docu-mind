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
