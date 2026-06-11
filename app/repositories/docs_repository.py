from typing import Tuple

from repositories.base_repository import BaseRepository


class DocsRepository(BaseRepository):
    """
    Implementación concreta de la capa de datos basada
    en documentos de texto simple
    """

    def __init__(self) -> None:
        self._memory: list[Tuple[int, str]] = []

    def __len__(self) -> int:
        return len(self._memory)

    def add(self, document: str) -> int:
        id = hash(document)
        self._memory.append((id, document))
        return id

    def retrieve(self, query: str) -> list[str]:
        results: list[str] = []
        for doc_tuple in self._memory:
            doc_text = doc_tuple[1]
            if query.lower() == doc_text:
                results.append(doc_text)

        return results
