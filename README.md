# 🧠 Personal Knowledge Base Chat

A fully local RAG (Retrieval-Augmented Generation) application that lets you upload PDF documents and chat with them using natural language — no API keys, no internet required.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Backend | FastAPI |
| RAG Framework | LangChain |
| LLM | Llama 3.2 (via Ollama) |
| Embeddings | nomic-embed-text (via Ollama) |
| Vector Store | ChromaDB (local) |

---

## How It Works

```
PDF Upload → Text Extraction → Chunking → Embedding → ChromaDB
                                                            ↓
User Question → Embed Question → Similarity Search → Top K Chunks
                                                            ↓
                                              LLM (Llama 3.2) → Answer
```

1. **Ingestion** — PDF is parsed, split into 500-token chunks, embedded using `nomic-embed-text`, and stored in a local ChromaDB collection.
2. **Retrieval** — User question is embedded and compared against stored chunks using cosine similarity. Top 4 relevant chunks are retrieved.
3. **Generation** — Retrieved chunks are passed as context to `llama3.2`, which generates a grounded answer.

---

## Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com/download) installed and running

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/your-username/knowledge-base-chat.git
cd knowledge-base-chat
```

### 2. Create and activate virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Pull Ollama models

```bash
ollama pull llama3.2
ollama pull nomic-embed-text
```

---

## Running the App

Open two terminals with the virtual environment activated.

**Terminal 1 — Backend**
```bash
cd backend
python -m uvicorn main:app --reload
```

Backend runs at `http://localhost:8000`
FastAPI docs available at `http://localhost:8000/docs`

**Terminal 2 — Frontend**
```bash
cd frontend
streamlit run app.py
```

Frontend runs at `http://localhost:8501`

---

## Project Structure

```
knowledge-base-chat/
├── backend/
│   ├── main.py            # FastAPI app — upload + query endpoints
│   ├── rag.py             # LangChain retrieval + generation pipeline
│   └── ingestor.py        # PDF parsing, chunking, embedding, storing
├── frontend/
│   └── app.py             # Streamlit UI
├── uploads/               # Temporary PDF storage (gitignored)
├── backend/chroma_store/  # ChromaDB persisted vectors (gitignored)
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Requirements

```
streamlit
fastapi
uvicorn
langchain
langchain-ollama
langchain-community
chromadb
pypdf
python-multipart
```

---

## Usage

1. Open `http://localhost:8501` in your browser
2. Upload any PDF using the file uploader
3. Wait for ingestion to complete (you'll see chunk count on success)
4. Type a question in the chat input
5. Get an answer grounded in your document

---

## Limitations

- **8GB RAM** — use `llama3.2` (3B) or `phi3` for best performance; larger models will be slow
- ChromaDB is persisted locally — restarting the app retains your ingested documents
- One document active per session (tracked via `st.session_state`)

---

## Future Improvements

- [ ] Multi-document support with a sidebar to switch between collections
- [ ] Source citation — show which chunks were used to answer
- [ ] Hybrid mode — switch between local Ollama and OpenAI via env variable
- [ ] Docker setup for one-command startup
- [ ] Conversation memory across multiple turns
