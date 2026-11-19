from datetime import date, datetime
from decimal import Decimal
from typing import ClassVar

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Identity,
    Numeric,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Basis(DeclarativeBase):
    type_annotation_map: ClassVar = {int: BigInteger}


class Bestelling(Basis):
    __tablename__ = "bestelling"

    id: Mapped[int] = mapped_column(Identity(), primary_key=True)
    klant_id: Mapped[int] = mapped_column(index=True)
    magazijn_id: Mapped[int]
    afleverklant_id: Mapped[int | None]
    factuurklant_id: Mapped[int | None]
    besteldatum: Mapped[date]
    gewenste_datum: Mapped[date | None]
    referentie: Mapped[str | None]
    inkoopordernummer: Mapped[str | None]
    status: Mapped[str]
    verzendnotities: Mapped[str | None]
    aangemaakt_op: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    bijgewerkt_op: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    regels: Mapped[list["Bestelregel"]] = relationship(
        cascade="all, delete-orphan", passive_deletes=True,
        lazy="selectin", order_by="Bestelregel.id",
    )


class Bestelregel(Basis):
    __tablename__ = "bestelregel"
    __table_args__ = (
        CheckConstraint("aantal > 0", name="ck_bestelregel_aantal"),
        CheckConstraint("stukprijs >= 0", name="ck_bestelregel_stukprijs"),
    )

    id: Mapped[int] = mapped_column(Identity(), primary_key=True)
    bestelling_id: Mapped[int] = mapped_column(
        ForeignKey("bestelling.id", ondelete="CASCADE"), index=True,
    )
    artikel_id: Mapped[str]
    aantal: Mapped[int]
    stukprijs: Mapped[Decimal | None] = mapped_column(Numeric(14, 2))
