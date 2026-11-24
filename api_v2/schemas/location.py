from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, StringConstraints


LocationCode = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=1,
        max_length=64,
        pattern=r"^[A-Za-z0-9-]+$",
    ),
]
LocationName = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=255),
]


class LocationCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    warehouse_id: Annotated[int, Field(gt=0)]
    code: LocationCode
    name: LocationName


class LocationUpdate(LocationCreate):
    pass


class LocationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    warehouse_id: int
    code: str
    name: str
    created_at: datetime
    updated_at: datetime
