from abc import abstractmethod, ABC

from fastapi import APIRouter


class AbstractRoute(ABC):

    @abstractmethod
    def map_routes(self) -> APIRouter:
        pass