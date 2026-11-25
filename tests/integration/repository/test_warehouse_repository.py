from datetime import datetime
from typing import List

import pytest
from sqlalchemy.exc import IntegrityError

from entity.warehouse import Warehouse
from repository.warehouse_repository import WarehouseRepository


def make_warehouse(code: str, name: str) -> Warehouse:
    return Warehouse(
        code=code,
        name=name,
        address="Teststraat 1",
        city="Rotterdam",
        zip_code="3011 AA",
        province="Zuid-Holland",
        country="Netherlands",
        contact_name="Test Contact",
        contact_phone="010-1234567",
        contact_email="contact@example.com",
        created_at=datetime(2026, 1, 1, 12, 0, 0),
    )


@pytest.fixture
def repository(db_session):
    yield WarehouseRepository(db_session.get_bind())

    db_session.rollback()
    db_session.query(Warehouse).delete()
    db_session.commit()


class TestWarehouseRepository:

    @pytest.fixture()
    def seed(self, db_session, repository) -> List[Warehouse]:
        warehouses = [
            make_warehouse("WH-ONE", "First warehouse"),
            make_warehouse("WH-TWO", "Second warehouse"),
        ]
        db_session.add_all(warehouses)
        db_session.commit()

        return warehouses

    def test_get_all_returns_every_warehouse(self, repository, seed):

        warehouses = repository.get_all()

        assert sorted(warehouse.code for warehouse in warehouses) == ["WH-ONE", "WH-TWO"]

    def test_get_all_returns_empty_list_when_there_are_no_warehouses(self, db_session, repository):
        warehouses = repository.get_all()

        assert len(warehouses) == 0

    def test_create_returns_new_warehouse_with_valid_entity(self, repository):
        warehouse: Warehouse = make_warehouse("WH-ONE", "New warehouse")

        new_warehouse = repository.create(warehouse)

        assert new_warehouse is not None
        assert new_warehouse.id is not None
        assert new_warehouse.code == "WH-ONE"

    def test_create_throws_exception_with_invalid_entity(self, repository):
        warehouse: Warehouse = Warehouse()

        with pytest.raises(IntegrityError):
            repository.create(warehouse)

    def test_update_returns_updated_warehouse_with_valid_entity(self, repository, seed):
        created = repository.create(make_warehouse("WH-ONE", "Old name"))

        changed = make_warehouse("WH-ONE", "New name")
        changed.id = created.id

        updated_warehouse = repository.update(changed)

        assert updated_warehouse is not None

        assert updated_warehouse.id == created.id
        assert updated_warehouse.name == "New name"
        assert updated_warehouse.updated_at is not None
        assert repository.get_by_id(created.id).name == "New name"

    def test_update_throws_exception_with_not_existing_entity(self, repository):
        unknown = make_warehouse("WH-ONE", "THIS DOES NOT EXISTS")
        unknown.id = 9999

        assert repository.update(unknown) is None

    def test_update_throws_exception_with_invalid_entity(self, repository):
        created = repository.create(make_warehouse("WH-ONE", "Old name"))

        changed = make_warehouse("WH-ONE", "Old name")
        changed.id = created.id
        changed.code = None

        with pytest.raises(IntegrityError):
            repository.update(changed)

    def test_get_by_id_returns_the_matching_warehouse(self, repository, seed):
        first_warehouse = seed[0]

        warehouse = repository.get_by_id(first_warehouse.id)

        assert warehouse is not None
        assert warehouse.id is not None
        assert warehouse.id == first_warehouse.id
        assert warehouse.code == "WH-ONE"

    def test_get_by_id_returns_none_when_id_does_not_exist(self, repository):
        warehouse = repository.get_by_id(999)

        assert warehouse is None

    def test_delete_returns_none_when_warehouse_deleted(self, repository, seed):
        warehouse = seed[0]

        status = repository.delete(warehouse.id)

        assert status is True

    def test_delete_returns_none_when_entity_does_not_exist(self, repository, seed):

        status = repository.delete(32432)

        assert status is None


