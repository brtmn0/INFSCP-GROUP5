from abc import ABC, abstractmethod
from typing import List

from entity.warehouse import Warehouse


class WarehouseRepositoryInterface(ABC):

    @abstractmethod
    def get_by_id(self, warehouse_id: int) -> Warehouse | None:
        """
            Retrieves a warehouse by its id

            Parameters:
                warehouse_id (int): The warehouse id

            Returns:
                warehouse Warehouse|None: The warehouse or None when no warehouse has this id
        """
        pass

    @abstractmethod
    def get_all(self) -> List[Warehouse]:
        """
            Retrieves all the warehouses

            Returns:
                warehouses List[Warehouse]: All warehouses or an empty lists when there are no warehouses
        """
        pass

    @abstractmethod
    def create(self, warehouse: Warehouse) -> Warehouse:
        """
            Creates a new warehouse

            Parameters:
                warehouse (Warehouse): The warehouse to create

            Returns:
                warehouse Warehouse: The warehouse created
        """
        pass

    @abstractmethod
    def update(self, warehouse: Warehouse) -> Warehouse | None:
        """
            Updates a warehouse

            Parameters:
                warehouse (Warehouse): The warehouse to update

            Returns:
                warehouse Warehouse|None: The warehouse updated or None when no warehouse has this id
        """
        pass

    @abstractmethod
    def delete(self, warehouse_id: int) -> bool | None:
        """
            Deletes a warehouse

            Parameters:
                warehouse_id (int): The warehouse id

            Returns:
                bool|None: True or None when no warehouse has this id

        """
        pass
