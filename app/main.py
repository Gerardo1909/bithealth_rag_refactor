from fastapi import FastAPI, HTTPException
from models import DocumentRequest, QuestionRequest
from rag_service import RagService
from repositories.docs_repository import DocsRepository
from repositories.qdrant_repository import QdrantRepository

app = FastAPI(title="Learning RAG Demo")

try:
    qdrant = QdrantRepository(collection_name="demo_collection")
    rag = RagService(qdrant)
except Exception as e:
    print("⚠️  Qdrant not available. Falling back to in-memory list.")
    memory_list = DocsRepository()
    rag = RagService(memory_list)


# --- API ENDPOINTS ---
@app.post("/ask")
def ask_question(req: QuestionRequest):
    try:
        return rag.retrieve(req.question)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/add")
def add_document(req: DocumentRequest):
    try:
        return rag.add_document(req.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/status")
def status():
    return {
        "qdrant_ready": rag.repository == "Qdrant",
        "in_memory_docs_count": len(memory_list),
        "service_ready": rag is not None,
    }
