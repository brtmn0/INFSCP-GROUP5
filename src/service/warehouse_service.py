import logging
from datetime import datetime

from dto.warehouse_request import WarehouseRequest
from entity.warehouse import Warehouse
from exceptions.warehouse_not_found_error import WarehouseNotFoundError
from repository.interface.warehouse_repository_interface import WarehouseRepositoryInterface
from service.interface.warehouse_service_interface import WarehouseServiceInterface

logger = logging.getLogger(__name__)

class WarehouseService(WarehouseServiceInterface):

    def __init__(self, warehouse_repository: WarehouseRepositoryInterface):
        self._warehouse_repository = warehouse_repository

    def get_all_warehouses(self, page: int) -> list[Warehouse]:
        offset = (page - 1) * 20
        warehouses = self._warehouse_repository.get_all(offset, 20)
        logger.debug("Retrieved %d warehouses", len(warehouses))
        return warehouses

    def get_warehouse_by_id(self, warehouse_id: int) -> Warehouse:
        warehouse = self._warehouse_repository.get_by_id(warehouse_id)
        if warehouse is None:
            raise WarehouseNotFoundError(warehouse_id)

        logger.debug("Retrieved warehouse with id %d", warehouse_id)
        return warehouse

    def update_warehouse(self, warehouse_id: int, warehouse_request: WarehouseRequest) -> Warehouse:
        existing_warehouse = self._warehouse_repository.get_by_id(warehouse_id)
        if existing_warehouse is None:
            raise WarehouseNotFoundError(warehouse_id)

        for key, value in warehouse_request.model_dump().items():
            setattr(existing_warehouse, key, value)

        updated_warehouse = self._warehouse_repository.update(existing_warehouse)
        if updated_warehouse is None:
            logger.error("Something went wrong updating warehouse with id %d.", existing_warehouse.id)
            return None

        logger.debug("Updated warehouse with id %d", existing_warehouse.id)
        return updated_warehouse

    def create_warehouse(self, warehouse_request: WarehouseRequest) -> Warehouse:
        new_warehouse = Warehouse(
            code=warehouse_request.code,
            name=warehouse_request.name,
            address=warehouse_request.address,
            city=warehouse_request.city,
            zip_code=warehouse_request.zip_code,
            province=warehouse_request.province,
            country=warehouse_request.country,
            contact_name=warehouse_request.contact_name,
            contact_phone=warehouse_request.contact_phone,
            contact_email=warehouse_request.contact_email,
            created_at=datetime.now(),
        )

        warehouse = self._warehouse_repository.create(new_warehouse)
        logger.debug("Created warehouse with id %d", warehouse.id)
        return warehouse

    def delete_warehouse(self, warehouse_id: int) -> bool:
        result = self._warehouse_repository.delete(warehouse_id)
        if result is None or result is False:
            raise WarehouseNotFoundError(warehouse_id)

        logger.debug("Deleted warehouse with id %d", warehouse_id)
        return True
