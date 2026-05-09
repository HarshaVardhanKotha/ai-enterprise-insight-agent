import chromadb
from openai import OpenAI
from sentence_transformers import SentenceTransformer
from config import (
    GROQ_API_KEY,
    GROQ_BASE_URL,
    CHROMA_PATH,
    COLLECTION_NAME,
    EMBEDDING_MODEL,
    CHAT_MODEL
)

embedding_model = SentenceTransformer(EMBEDDING_MODEL)

def get_groq_client():
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY not found. Add it to your .env file.")

    return OpenAI(
        api_key=GROQ_API_KEY,
        base_url=GROQ_BASE_URL
    )

def create_query_embedding(query: str):
    return embedding_model.encode(query).tolist()

def retrieve_context(query: str, top_k: int = 4):
    chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = chroma_client.get_or_create_collection(name=COLLECTION_NAME)

    query_embedding = create_query_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    contexts = results["documents"][0] if results["documents"] else []
    sources = results["metadatas"][0] if results["metadatas"] else []

    return contexts, sources

def answer_with_rag(query: str):
    client = get_groq_client()

    contexts, sources = retrieve_context(query)
    context_text = "\n\n".join(contexts)

    system_prompt = (
        "You are an enterprise AI assistant. "
        "Use only the retrieved enterprise context to answer. "
        "If the context is insufficient, clearly say so. "
        "Keep answers concise, grounded, and business-friendly."
    )

    user_prompt = f'''
User question:
{query}

Retrieved enterprise context:
{context_text}

Provide:
1. Direct answer
2. Supporting context
3. Suggested next step if useful
'''

    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content, sources
