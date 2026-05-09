# AI Enterprise Insight Agent

A clean Generative AI portfolio project that demonstrates Retrieval-Augmented Generation, semantic search, vector databases, structured-data analysis, and simple agentic planning.

This version uses **Groq with Llama 3.3 70B Versatile** for chat completions and **Sentence Transformers** for local embeddings.

## What It Does

The app helps users ask questions over company knowledge and business data.

It supports:
- Enterprise Knowledge Q&A using RAG
- Business Metrics Analysis using CSV data
- AI Action Planner using Groq/Llama

## Architecture

```text
User Query
   ↓
Sentence Transformer Embedding
   ↓
ChromaDB Vector Search
   ↓
Retrieved Enterprise Context
   ↓
Groq / Llama Prompt
   ↓
Grounded Answer + Action Plan
```

## Tech Stack

Python, Streamlit, ChromaDB, Groq API, Llama 3.3 70B Versatile, OpenAI-compatible client, Sentence Transformers, Pandas, NumPy, python-dotenv.

## Setup

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Add your Groq API key in `.env`:

```text
GROQ_API_KEY=your_groq_api_key_here
CHROMA_PATH=./chroma_db
COLLECTION_NAME=enterprise_knowledge
```

## Run

```bash
python ingest.py
streamlit run app.py
```

## Example Questions

```text
What are the AI governance rules?
How should customer complaints be escalated?
What are the main operational risks?
Why did customer satisfaction decrease in the South region?
```

## Resume Bullet

Built an AI Enterprise Insight Agent using Python, Streamlit, Groq/Llama, ChromaDB, sentence-transformer embeddings, and RAG to retrieve enterprise context, analyze structured business metrics, and generate grounded AI action plans.
