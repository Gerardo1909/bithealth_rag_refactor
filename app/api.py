from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from models import DocumentRequest, QuestionRequest
from rag_service import RagService
from repositories.docs_repository import DocsRepository
from repositories.qdrant_repository import QdrantRepository

# Tradeoff aceptado
try:
    qdrant = QdrantRepository(collection_name="demo_collection")
    _GLOBAL_RAG_SERVICE = RagService(qdrant)
except Exception as e:
    print("⚠️ Qdrant not available. Falling back to global in-memory list.")
    memory_list = DocsRepository()
    _GLOBAL_RAG_SERVICE = RagService(memory_list)


def get_rag_service() -> RagService:
    return _GLOBAL_RAG_SERVICE


router = APIRouter()


@router.post("/ask")
def ask_question(
    req: QuestionRequest, rag: Annotated[RagService, Depends(get_rag_service)]
):
    try:
        return rag.retrieve(req.question)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/add")
def add_document(
    req: DocumentRequest, rag: Annotated[RagService, Depends(get_rag_service)]
):
    try:
        return rag.add_document(req.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
def status(rag: Annotated[RagService, Depends(get_rag_service)]):
    return {
        "qdrant_ready": rag.repository == "Qdrant",
        "in_memory_docs_count": rag.documents_length,
        "service_ready": rag is not None,
    }
