from datetime import datetime

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from entity.warehouse import Warehouse
from exceptions.exception_handlers import register_exception_handlers
from repository.warehouse_repository import WarehouseRepository
from routes.warehouse_routes import WarehouseRoutes
from service.warehouse_service import WarehouseService

UNKNOWN_ID = 9999
NOT_FOUND_BODY = {"detail": f"Warehouse with id {UNKNOWN_ID} was not found"}


def make_body(code: str, name: str) -> dict:
    return {
        "warehouse": {
            "code": code,
            "name": name,
            "address": "Teststraat 1",
            "city": "Rotterdam",
            "zip_code": "3011 AA",
            "province": "Zuid-Holland",
            "country": "Netherlands",
            "contact_name": "Test Contact",
            "contact_phone": "010-1234567",
            "contact_email": "contact@example.com",
        }
    }


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
def client(db_session):
    """A test client for an app with the warehouse routes, connected to the test database."""
    repository = WarehouseRepository(db_session.get_bind())
    service = WarehouseService(repository)

    app = FastAPI()
    register_exception_handlers(app)
    app.include_router(WarehouseRoutes(service).map_routes())

    yield TestClient(app)

    db_session.rollback()
    db_session.query(Warehouse).delete()
    db_session.commit()


@pytest.fixture
def seed(db_session, client):
    warehouses = [
        make_warehouse("WH-ONE", "First warehouse"),
        make_warehouse("WH-TWO", "Second warehouse"),
    ]
    db_session.add_all(warehouses)
    db_session.commit()

    return warehouses


class TestWarehouseRoutes:

    def test_get_all_warehouses_returns_200_with_every_warehouse(self, client, seed):
        response = client.get("/warehouses/")

        assert response.status_code == 200
        assert sorted(warehouse["code"] for warehouse in response.json()) == ["WH-ONE", "WH-TWO"]

    def test_get_all_warehouses_returns_empty_list_when_there_are_no_warehouses(self, client):
        response = client.get("/warehouses/")

        assert response.status_code == 200
        assert response.json() == []

    def test_get_warehouse_by_id_returns_200_with_the_warehouse(self, client, seed):
        first = seed[0]

        response = client.get(f"/warehouses/{first.id}")

        assert response.status_code == 200
        assert response.json()["id"] == first.id
        assert response.json()["code"] == "WH-ONE"

    def test_get_warehouse_by_id_returns_422_when_id_is_below_one(self, client):
        response = client.get("/warehouses/0")

        assert response.status_code == 422

    def test_get_warehouse_by_id_returns_404_when_warehouse_does_not_exist(self, client):
        response = client.get(f"/warehouses/{UNKNOWN_ID}")

        assert response.status_code == 404
        assert response.json() == NOT_FOUND_BODY

    def test_create_warehouse_returns_201_with_the_new_warehouse(self, client):
        response = client.post("/warehouses/", json=make_body("WH-NEW", "New warehouse"))

        assert response.status_code == 201
        assert response.json()["id"] is not None
        assert response.json()["code"] == "WH-NEW"

    def test_create_warehouse_stores_the_warehouse(self, client):
        created = client.post("/warehouses/", json=make_body("WH-NEW", "New warehouse")).json()

        response = client.get(f"/warehouses/{created['id']}")

        assert response.status_code == 200
        assert response.json()["name"] == "New warehouse"

    def test_create_warehouse_returns_422_when_a_field_is_missing(self, client):
        body = make_body("WH-NEW", "New warehouse")
        del body["warehouse"]["code"]

        response = client.post("/warehouses/", json=body)

        assert response.status_code == 422

    def test_update_warehouse_returns_200_with_the_updated_warehouse(self, client, seed):
        first = seed[0]

        response = client.put(f"/warehouses/{first.id}", json=make_body("WH-ONE", "Renamed warehouse"))

        assert response.status_code == 200
        assert response.json()["id"] == first.id
        assert response.json()["name"] == "Renamed warehouse"

    def test_update_warehouse_returns_404_when_warehouse_does_not_exist(self, client):
        response = client.put(f"/warehouses/{UNKNOWN_ID}", json=make_body("WH-ONE", "Renamed warehouse"))

        assert response.status_code == 404
        assert response.json() == NOT_FOUND_BODY

    def test_delete_warehouse_returns_204_and_removes_the_warehouse(self, client, seed):
        first = seed[0]

        response = client.delete(f"/warehouses/{first.id}")

        assert response.status_code == 204
        assert client.get(f"/warehouses/{first.id}").status_code == 404

    def test_delete_warehouse_returns_404_when_warehouse_does_not_exist(self, client):
        response = client.delete(f"/warehouses/{UNKNOWN_ID}")

        assert response.status_code == 404
        assert response.json() == NOT_FOUND_BODY
