from abc import ABC


class BaseRepository(ABC):
    """
    Clase que representa el comportamiento de la capa de datos
    del sistema.
    """

    def __len__(self) -> int:
        raise NotImplementedError

    def __str__(self) -> str:
        raise NotImplementedError

    def add(self, document: str) -> int:
        raise NotImplementedError

    def retrieve(self, query: str) -> list[str]:
        raise NotImplementedError
