from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil, os
from ingestor import ingest_pdf
from rag import get_answer

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str
    collection_name: str

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    file_path = f"../uploads/{file.filename}"
    os.makedirs("../uploads", exist_ok=True)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    collection_name = file.filename.replace(".pdf", "").replace(" ", "_")
    chunk_count = ingest_pdf(file_path, collection_name)
    return {"message": "Ingested", "chunks": chunk_count,
            "collection": collection_name}

@app.post("/query")
async def query(req: QueryRequest):
    answer = get_answer(req.question, req.collection_name)
    return {"answer": answer}