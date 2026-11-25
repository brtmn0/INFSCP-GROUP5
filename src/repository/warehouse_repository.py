from datetime import datetime
from typing import List, override

from sqlalchemy import select, Engine
from sqlalchemy.orm import Session

from entity.warehouse import Warehouse
from repository.interface.warehouse_repository_interface import WarehouseRepositoryInterface


class WarehouseRepository(WarehouseRepositoryInterface):
    table = "warehouse"
    entity = Warehouse

    def __init__(self, engine: Engine):
        self.engine = engine

    def get_by_id(self, warehouse_id: int) -> Warehouse | None:
        with Session(self.engine) as session:
            return session.get(Warehouse, warehouse_id)

    def get_all(self) -> List[Warehouse]:
        stmt = select(Warehouse)
        with Session(self.engine) as session:
            return list(session.scalars(stmt).all())

    def create(self, warehouse: Warehouse) -> Warehouse:
        with Session(self.engine) as session:
            session.add(warehouse)
            session.commit()
            session.refresh(warehouse)

            return warehouse

    def update(self, warehouse: Warehouse) -> Warehouse | None:
        with Session(self.engine) as session:
            if session.get(Warehouse, warehouse.id) is None:
                return None

            merged = session.merge(warehouse)
            merged.updated_at = datetime.now()
            session.commit()
            session.refresh(merged)

            return merged

    def delete(self, warehouse_id: int) -> bool | None:
        with Session(self.engine) as session:
            if session.get(Warehouse, warehouse_id) is None:
                return None

            session.delete(session.get(Warehouse, warehouse_id))
            session.commit()

            return True



