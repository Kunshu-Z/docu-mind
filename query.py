import ollama
import chromadb

client = chromadb.PersistentClient(path="db")
collection = client.get_or_create_collection("docs")

# Embed text using the Ollama embeddings model
def embed(text):
    return ollama.embeddings(model="nomic-embed-text", prompt=text)["embedding"]

# Retrieve the most relevant chunks for a given question
def retrieve(question, n=3):
    results = collection.query(query_embeddings=[embed(question)], n_results=n)
    chunks, metas = results["documents"][0], results["metadatas"][0]
    print("--- Retrieved chunks ---")
    for c, m in zip(chunks, metas):
        print(f"metadata: {m}")
        print(f"chunk: {c}")
    print("------------------------")
    return chunks, metas

# Answer a question using the retrieved chunks as context
def answer(question):
    chunks, metas = retrieve(question)
    context = "\n\n".join(chunks)
    prompt = f"""Answer the question using only the context below. If the answer isn't in the context, say "I don't know based on the provided documents."

Context:
{context}

Question: {question}"""

    response = ollama.chat(
        model="llama3.2",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["message"]["content"]

if __name__ == "__main__":
    question = input("What is your question? ")
    print(answer(question))