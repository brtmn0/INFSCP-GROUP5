from datetime import datetime
from typing import TypeVar, Type, List

from sqlalchemy import Engine, select
from sqlalchemy.orm import Session

from entity.base import Base
from repository.interface.base_repository_interface import BaseRepositoryInterface

# Bound to base so ONLY entities that inherit BASE are accepted!
T = TypeVar('T', bound=Base)

class BaseRepository(BaseRepositoryInterface[T]):

    def __init__(self, engine: Engine, entity: Type[T]):
        self.engine = engine
        self.entity = entity

    def get_by_id(self, entity_id: int) -> T|None:
        with Session(self.engine) as session:
            return session.get(self.entity, entity_id)

    def get_all(self, offset: int = 0, limit: int = 20) -> List[T]:
        stmt = select(self.entity).offset(offset).limit(limit)
        with Session(self.engine) as session:
            return list(session.scalars(stmt).all())

    def create(self, entity: T) -> T:
        with Session(self.engine) as session:
            session.add(entity)
            session.commit()
            session.refresh(entity)

            return entity

    def update(self, entity: T) -> T | None:
        with Session(self.engine) as session:
            if session.get(self.entity, entity.id) is None:
                return None

            merged = session.merge(entity)
            merged.updated_at = datetime.now()
            session.commit()
            session.refresh(merged)

            return merged

    def delete(self, entity_id: int) -> bool | None:
        with Session(self.engine) as session:
            if session.get(self.entity, entity_id) is None:
                return None

            session.delete(session.get(self.entity, entity_id))
            session.commit()

            return True

