from abc import ABC


class BaseRepository(ABC):
    """
    Clase que representa el comportamiento de la capa de datos
    del sistema.
    """

    def add(self, document: str) -> int:
        raise NotImplementedError

    def retrieve(self, query: str) -> list[str]:
        raise NotImplementedError
