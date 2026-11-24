from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import Session

from api_v2.database import Base
from api_v2.models import Location, Warehouse


def test_location_model_has_required_warehouse_relationship():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        warehouse = Warehouse(id=1)
        session.add(warehouse)
        session.flush()

        first = Location(warehouse=warehouse, code="DUP-1", name="First")
        second = Location(warehouse=warehouse, code="DUP-1", name="Second")
        session.add_all([first, second])
        session.commit()

        assert first.id is not None
        assert first.created_at is not None
        assert first.updated_at is not None
        assert [location.id for location in warehouse.locations] == [first.id, second.id]

    location_table = inspect(engine).get_columns("locations")
    assert {column["name"] for column in location_table} == {
        "id",
        "warehouse_id",
        "code",
        "name",
        "created_at",
        "updated_at",
    }
