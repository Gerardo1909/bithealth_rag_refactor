import random

from base_repository import BaseRepository
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams


class QdrantRepository(BaseRepository):
    """
    Implementación concreta de la capa de datos hecha en
    Qdrant
    """

    def __init__(self) -> None:
        self.qdrant = QdrantClient("http://localhost:6333")
        self.qdrant.recreate_collection(
            collection_name="demo_collection",
            vectors_config=VectorParams(size=128, distance=Distance.COSINE),
        )

    def add(self, document: str) -> int:
        doc_emb = self._embed(document)
        id = hash(document)
        self.qdrant.upsert(
            collection_name="demo_collection",
            points=[PointStruct(id=id, vector=doc_emb, payload=document)],
        )
        return id

    def retrieve(self, query: str) -> list[str]:
        results: list[str] = []
        query_emb = self._embed(query)

        hits = self.qdrant.search(
            collection_name="demo_collection", query_vector=query_emb, limit=2
        )
        for hit in hits:
            results.append(hit.payload["text"])

        return results

    def _embed(self, query: str) -> list[float]:
        random.seed(abs(hash(query)) % 10000)
        return [random.random() for _ in range(128)]
