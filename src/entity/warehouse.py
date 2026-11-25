from datetime import datetime
from typing import Optional

from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from entity.base import Base


class Warehouse(Base):
    __tablename__ = "warehouse"

    code: Mapped[str] = mapped_column(String(30))
    name: Mapped[str] = mapped_column(String(100))
    address: Mapped[str] = mapped_column(String(255))
    city: Mapped[str] = mapped_column(String(255))
    zip_code: Mapped[str] = mapped_column(String(10))
    province: Mapped[str] = mapped_column(String(255))
    country:  Mapped[str] = mapped_column(String(255))
    contact_name:  Mapped[str] = mapped_column(String(255))
    contact_phone:  Mapped[str] = mapped_column(String(255))
    contact_email:  Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime)
    updated_at: Mapped[Optional[datetime]]