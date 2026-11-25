from sqlalchemy import Engine

from entity.warehouse import Warehouse
from repository.base_repository import BaseRepository
from repository.interface.warehouse_repository_interface import WarehouseRepositoryInterface


class WarehouseRepository(BaseRepository[Warehouse], WarehouseRepositoryInterface):
    table = "warehouse"
    entity = Warehouse

    def __init__(self, engine: Engine):
        super().__init__(engine, Warehouse)





