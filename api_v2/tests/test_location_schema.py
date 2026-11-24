import pytest
from pydantic import ValidationError

from api_v2.schemas.location import LocationCreate


def test_location_create_accepts_valid_payload():
    location = LocationCreate(
        warehouse_id=1,
        code="VGH-AMB-B12-R6-B7",
        name="Zone B Aisle 12 Rack 6 Bin 7",
    )

    assert location.model_dump() == {
        "warehouse_id": 1,
        "code": "VGH-AMB-B12-R6-B7",
        "name": "Zone B Aisle 12 Rack 6 Bin 7",
    }


@pytest.mark.parametrize(
    "payload",
    [
        {"warehouse_id": 0, "code": "LOC-1", "name": "Location"},
        {"warehouse_id": 1, "code": "LOC/1", "name": "Location"},
        {"warehouse_id": 1, "code": "LOC-1", "name": "  "},
        {"warehouse_id": 1, "code": "LOC-1", "name": "Location", "id": 9},
    ],
)
def test_location_create_rejects_invalid_payload(payload):
    with pytest.raises(ValidationError):
        LocationCreate.model_validate(payload)
