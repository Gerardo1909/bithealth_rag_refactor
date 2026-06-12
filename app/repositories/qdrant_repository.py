import random
import uuid

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams
from repositories.base_repository import BaseRepository


class QdrantRepository(BaseRepository):
    """
    Implementación concreta de la capa de datos hecha en
    Qdrant
    """

    def __init__(
        self, collection_name: str, port: str = "http://localhost:6333"
    ) -> None:
        self.collection_name = collection_name
        self.qdrant = QdrantClient(url=port)
        self.qdrant.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=128, distance=Distance.COSINE),
        )

    def __str__(self) -> str:
        return "Qdrant"

    def __len__(self) -> int:
        result = self.qdrant.count(collection_name=self.collection_name, exact=True)
        return result.count

    def add(self, document: str) -> int:
        doc_emb = self._embed(document)
        id = uuid.uuid4().int
        doc_payload = {"text": document}
        self.qdrant.upsert(
            collection_name=self.collection_name,
            points=[PointStruct(id=id, vector=doc_emb, payload=doc_payload)],
        )
        return id

    def retrieve(self, query: str) -> list[str]:
        results: list[str] = []
        query_emb = self._embed(query)

        hits = self.qdrant.search(
            collection_name=self.collection_name, query_vector=query_emb, limit=2
        )
        for hit in hits:
            results.append(hit.payload["text"])

        return results

    def _embed(self, query: str) -> list[float]:
        random.seed(abs(hash(query)) % 10000)
        return [random.random() for _ in range(128)]
