from abc import ABC, abstractmethod
from typing import List, TypeVar, Generic
from xml.dom.minidom import Entity

from entity.base import Base

# Bound to base so ONLY entities that inherit BASE are accepted!
T = TypeVar("T", bound=Base)

class BaseRepositoryInterface(ABC, Generic[T]):

    @abstractmethod
    def get_by_id(self, entity_id: int) -> T|None:
        """
            Retrieves an entity by its id

            Parameters:
                entity_id (int): The entity id

            Returns:
                 Entity|None: The Entity or None when no Entity has this id
        """
        pass

    @abstractmethod
    def get_all(self, offset: int = 0, limit: int = 20) -> List[T]:
        """
            Retrieves all the entities

            Parameters:
                offset (int): The offset to start with
                limit (int): The number of entities to return

            Returns:
                entities List[T]: All entities or an empty lists when there are no entities
        """
        pass

    @abstractmethod
    def create(self, entity: T) -> T:
        """
            Creates a new entity

            Parameters:
                entity (T): The entity to create

            Returns:
                entity T: The entity created
        """
        pass

    @abstractmethod
    def update(self, entity: T) -> T|None:
        """
            Updates an entity

            Parameters:
                entity (T): The entity to update

            Returns:
                entity T|None: The entity updated or None when no entity has this id
        """
        pass

    @abstractmethod
    def delete(self, entity_id: int) -> bool|None:
        """
            Deletes an entity

            Parameters:
                entity_id (int): The entity id

            Returns:
                bool|None: True or None when no entity has this id

        """
        pass
