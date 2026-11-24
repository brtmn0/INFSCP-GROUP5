from typing import TYPE_CHECKING

from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api_v2.database import Base

if TYPE_CHECKING:
    from api_v2.models.location import Location


class Warehouse(Base):
    __tablename__ = "warehouses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    locations: Mapped[list["Location"]] = relationship(
        back_populates="warehouse",
        passive_deletes=True,
    )
