from unittest.mock import Mock

import pytest

from dto.warehouse_request import WarehouseRequest
from entity.warehouse import Warehouse
from exceptions.warehouse_not_found_error import WarehouseNotFoundError
from repository.interface.warehouse_repository_interface import WarehouseRepositoryInterface
from service.warehouse_service import WarehouseService


def make_request() -> WarehouseRequest:
    return WarehouseRequest(
        code="WH-001",
        name="Warehouse Rotterdam",
        address="Wijnhaven 107",
        city="Rotterdam",
        zip_code="3011 WN",
        province="Zuid-Holland",
        country="Netherlands",
        contact_name="John Doe",
        contact_phone="+31 612345678",
        contact_email="john.doe@example.com",
    )


@pytest.fixture
def repository():
    return Mock(spec=WarehouseRepositoryInterface)


@pytest.fixture
def service(repository):
    return WarehouseService(repository)


class TestWarehouseService:

    def test_get_all_warehouses_returns_the_warehouses_from_the_repository(self, service, repository):
        warehouses = [Warehouse(id=1, code="WH-ONE"), Warehouse(id=2, code="WH-TWO")]
        repository.get_all.return_value = warehouses

        assert service.get_all_warehouses() == warehouses

    def test_get_warehouse_by_id_returns_the_warehouse_from_the_repository(self, service, repository):
        warehouse = Warehouse(id=1, code="WH-ONE")
        repository.get_by_id.return_value = warehouse

        assert service.get_warehouse_by_id(1) is warehouse

    def test_get_warehouse_by_id_raises_not_found_when_warehouse_does_not_exist(self, service, repository):
        repository.get_by_id.return_value = None

        with pytest.raises(WarehouseNotFoundError):
            service.get_warehouse_by_id(1)

    def test_create_warehouse_returns_the_warehouse_from_the_repository(self, service, repository):
        created = Warehouse(id=1, code="WH-001")
        repository.create.return_value = created

        assert service.create_warehouse(make_request()) is created

    def test_create_warehouse_saves_a_warehouse_with_the_request_fields(self, service, repository):
        repository.create.return_value = Warehouse(id=1)

        service.create_warehouse(make_request())

        saved = repository.create.call_args.args[0]
        assert saved.code == "WH-001"
        assert saved.name == "Warehouse Rotterdam"
        assert saved.created_at is not None

    def test_update_warehouse_applies_the_request_fields(self, service, repository):
        existing = Warehouse(id=1, code="OLD", name="Old name")
        repository.get_by_id.return_value = existing
        repository.update.return_value = existing

        updated = service.update_warehouse(1, make_request())

        assert updated.code == "WH-001"
        assert updated.name == "Warehouse Rotterdam"

    def test_update_warehouse_raises_not_found_when_warehouse_does_not_exist(self, service, repository):
        repository.get_by_id.return_value = None

        with pytest.raises(WarehouseNotFoundError):
            service.update_warehouse(1, make_request())

        repository.update.assert_not_called()

    def test_delete_warehouse_returns_true_when_warehouse_is_deleted(self, service, repository):
        repository.delete.return_value = True

        assert service.delete_warehouse(1) is True

    def test_delete_warehouse_raises_not_found_when_warehouse_does_not_exist(self, service, repository):
        repository.delete.return_value = None

        with pytest.raises(WarehouseNotFoundError):
            service.delete_warehouse(1)
