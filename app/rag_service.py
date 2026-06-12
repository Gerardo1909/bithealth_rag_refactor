import time
from typing import Any

from repositories.base_repository import BaseRepository


class RagService:
    def __init__(self, repository: BaseRepository) -> None:
        self._repository = repository

    @property
    def repository(self) -> str:
        return str(self._repository)

    @property
    def documents_length(self) -> int:
        return len(self._repository)

    def retrieve(self, query: str) -> dict[str, Any]:
        try:
            start = time.time()
            results = self._repository.retrieve(query)
            return {
                "question": query,
                "answer": results[0] if results else [],
                "context_used": results,
                "latency_sec": round(time.time() - start, 3),
            }
        except Exception as e:
            raise RagException(f"Ha ocurrido un error en el servicio: {str(e)}")

    def add_document(self, document: str) -> dict[str, Any]:
        try:
            doc_id = self._repository.add(document)
            return {"id": doc_id, "status": "added"}
        except Exception as e:
            raise RagException(f"Ha ocurrido un error en el servicio: {str(e)}")


class RagException(Exception):
    """
    Excepción base para el servicio RAG
    """

    pass
