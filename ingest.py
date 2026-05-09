from pathlib import Path
import uuid
import chromadb
from sentence_transformers import SentenceTransformer
from config import CHROMA_PATH, COLLECTION_NAME, EMBEDDING_MODEL

embedding_model = SentenceTransformer(EMBEDDING_MODEL)

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 80):
    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        chunk = " ".join(words[start:start + chunk_size])
        chunks.append(chunk)
        start += chunk_size - overlap

    return chunks

def create_embedding(text: str):
    return embedding_model.encode(text).tolist()

def load_docs(folder="docs"):
    documents = []

    for file_path in Path(folder).glob("*.txt"):
        text = file_path.read_text(encoding="utf-8")
        chunks = chunk_text(text)

        for index, chunk in enumerate(chunks):
            documents.append({
                "id": str(uuid.uuid4()),
                "text": chunk,
                "source": file_path.name,
                "chunk_index": index
            })

    return documents

def main():
    chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = chroma_client.get_or_create_collection(name=COLLECTION_NAME)

    documents = load_docs()

    if not documents:
        print("No text documents found in docs/")
        return

    ids, texts, metadatas, embeddings = [], [], [], []

    for doc in documents:
        ids.append(doc["id"])
        texts.append(doc["text"])
        metadatas.append({
            "source": doc["source"],
            "chunk_index": doc["chunk_index"]
        })
        embeddings.append(create_embedding(doc["text"]))

    collection.upsert(
        ids=ids,
        documents=texts,
        metadatas=metadatas,
        embeddings=embeddings
    )

    print(f"Ingested {len(documents)} document chunks into collection: {COLLECTION_NAME}")

if __name__ == "__main__":
    main()
