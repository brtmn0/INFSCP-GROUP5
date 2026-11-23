from abc import ABC, abstractmethod

from dto.warehouse_request import WarehouseRequest
from entity.warehouse import Warehouse


class WarehouseServiceInterface(ABC):

    @abstractmethod
    def get_all_warehouses(self) -> list[Warehouse]:
        """
            Retrieves all the warehouses

            Returns:
                warehouses list[Warehouse]: List of all the warehouses
        """
        pass

    @abstractmethod
    def get_warehouse_by_id(self, warehouse_id: int) -> Warehouse:
        """
            Retrieves a warehouse by its id

            Parameters:
                warehouse_id (int): The warehouse id

            Returns:
                warehouse Warehouse|None: The warehouse
        """
        pass

    @abstractmethod
    def update_warehouse(self, warehouse_id: int, warehouse_request: WarehouseRequest) -> Warehouse:
        """
            Updates an existing warehouse

            Parameters:
                warehouse_id (int): The warehouse id to update
                warehouse_request (WarehouseRequest): The warehouse fields to update

            Returns:
                warehouse Warehouse|None: The updated warehouse
        """
        pass

    @abstractmethod
    def create_warehouse(self, warehouse_request: WarehouseRequest) -> Warehouse:
        """
            Creates a new warehouse

            Parameters:
                warehouse_request (WarehouseRequest): The warehouse to create

            Returns:
                warehouse Warehouse|None: The created warehouse
        """
        pass

    @abstractmethod
    def delete_warehouse(self, warehouse_id: int) -> bool:
        """
            Deletes an existing warehouse

            Parameters:
                warehouse_id (int): The warehouse id

            Returns:
                bool: True if the warehouse was successfully deleted otherwise False
        """
        pass
