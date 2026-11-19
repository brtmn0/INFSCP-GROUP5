import os
from collections.abc import Iterator
from contextlib import asynccontextmanager
from datetime import UTC, date, datetime
from decimal import Decimal
from secrets import compare_digest
from typing import Annotated, Literal

from fastapi import APIRouter, Depends, FastAPI, HTTPException, Path, Response, Security
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, ConfigDict, Field, StringConstraints
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from cargohub.database import Bestelling, Bestelregel

PositiefGeheel = Annotated[int, Field(gt=0, le=2**63 - 1, strict=True)]
BestellingId = Annotated[int, Path(gt=0, le=2**63 - 1)]
KorteTekst = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=255)]
Rol = Literal["gebruiker", "beheerder"]

router = APIRouter(prefix="/api/v1/bestellingen", tags=["Bestellingen"])
sleutel_header = APIKeyHeader(name="API_KEY", auto_error=False)


class BestelregelGegevens(BaseModel):
    model_config = ConfigDict(extra="forbid", from_attributes=True)

    artikel_id: KorteTekst
    aantal: PositiefGeheel
    stukprijs: Annotated[Decimal, Field(ge=0, max_digits=14, decimal_places=2)] | None = None


class BestellingGegevens(BaseModel):
    model_config = ConfigDict(extra="forbid", from_attributes=True)

    klant_id: PositiefGeheel
    magazijn_id: PositiefGeheel
    afleverklant_id: PositiefGeheel | None = None
    factuurklant_id: PositiefGeheel | None = None
    besteldatum: date
    gewenste_datum: date | None = None
    referentie: KorteTekst | None = None
    inkoopordernummer: KorteTekst | None = None
    verzendnotities: Annotated[str, Field(max_length=4000)] | None = None


class NieuweBestelling(BestellingGegevens):
    regels: list[BestelregelGegevens] = Field(default_factory=list, max_length=1000)


class BestellingWijziging(BestellingGegevens):
    status: KorteTekst
    regels: Annotated[list[BestelregelGegevens], Field(max_length=1000)] | None = None


class BestellingAntwoord(BestellingGegevens):
    id: int
    status: str
    regels: list[BestelregelGegevens]
    aangemaakt_op: datetime
    bijgewerkt_op: datetime


def maak_app(database_url: str, gebruikerssleutel: str, beheerderssleutel: str) -> FastAPI:
    if not gebruikerssleutel or not beheerderssleutel or gebruikerssleutel == beheerderssleutel:
        raise ValueError("Configureer twee verschillende, niet-lege API-sleutels.")
    engine = create_engine(database_url, pool_pre_ping=True)
    @asynccontextmanager
    async def levensduur(_app: FastAPI):
        try:
            yield
        finally:
            engine.dispose()

    app = FastAPI(title="CargoHub Bestellingen", lifespan=levensduur)
    def open_sessie() -> Iterator[Session]:
        with Session(engine, expire_on_commit=False) as sessie:
            yield sessie

    app.dependency_overrides[database_sessie] = open_sessie

    def controleer_sleutel(sleutel: Annotated[str | None, Security(sleutel_header)]) -> Rol:
        invoer = (sleutel or "").encode()
        if compare_digest(invoer, beheerderssleutel.encode()):
            return "beheerder"
        if compare_digest(invoer, gebruikerssleutel.encode()):
            return "gebruiker"
        raise HTTPException(401, "Ongeldige of ontbrekende API-sleutel.")

    app.dependency_overrides[authenticatie] = controleer_sleutel

    @app.exception_handler(RequestValidationError)
    async def ongeldige_invoer(_, fout: RequestValidationError) -> JSONResponse:
        details = [
            {"veld": list(probleem["loc"]), "code": probleem["type"]}
            for probleem in fout.errors()
        ]
        return JSONResponse(status_code=400, content={"detail": "Ongeldige invoer.", "velden": details})

    app.include_router(router)
    return app


def maak_app_uit_omgeving() -> FastAPI:
    return maak_app(
        os.environ["DATABASE_URL"],
        os.environ["CARGOHUB_GEBRUIKERSSLEUTEL"],
        os.environ["CARGOHUB_BEHEERDERSSLEUTEL"],
    )


def database_sessie() -> Iterator[Session]:
    raise RuntimeError("Databasesessie is niet geconfigureerd.")


def authenticatie(sleutel: Annotated[str | None, Security(sleutel_header)]) -> Rol:
    raise RuntimeError("Authenticatie is niet geconfigureerd.")


def vereis_beheerder(rol: Annotated[Rol, Depends(authenticatie)]) -> None:
    if rol != "beheerder":
        raise HTTPException(403, "Deze actie vereist beheerdersrechten.")


Sessie = Annotated[Session, Depends(database_sessie)]
Ingelogd = [Depends(authenticatie)]
Beheerder = [Depends(vereis_beheerder)]


def haal_bestelling(sessie: Session, bestelling_id: int, *, vergrendel: bool = False) -> Bestelling:
    bestelling = sessie.get(Bestelling, bestelling_id, with_for_update=vergrendel)
    if bestelling is None:
        raise HTTPException(404, "Bestelling niet gevonden.")
    return bestelling


def vervang_regels(bestelling: Bestelling, regels: list[BestelregelGegevens]) -> None:
    bestelling.regels = [Bestelregel(**regel.model_dump()) for regel in regels]


@router.get("", response_model=list[BestellingAntwoord], dependencies=Ingelogd)
def lijst_bestellingen(sessie: Sessie):
    return sessie.scalars(select(Bestelling).order_by(Bestelling.id)).all()


@router.get("/{bestelling_id}", response_model=BestellingAntwoord, dependencies=Ingelogd)
def lees_bestelling(bestelling_id: BestellingId, sessie: Sessie):
    return haal_bestelling(sessie, bestelling_id)


@router.get("/{bestelling_id}/regels", response_model=list[BestelregelGegevens], dependencies=Ingelogd)
def lees_bestelregels(bestelling_id: BestellingId, sessie: Sessie):
    return haal_bestelling(sessie, bestelling_id).regels


@router.post("", response_model=BestellingAntwoord, status_code=201, dependencies=Ingelogd)
def plaats_bestelling(invoer: NieuweBestelling, sessie: Sessie, antwoord: Response):
    bestelling = Bestelling(**invoer.model_dump(exclude={"regels"}), status="geplaatst")
    vervang_regels(bestelling, invoer.regels)
    sessie.add(bestelling)
    sessie.commit()
    antwoord.headers["Location"] = f"/api/v1/bestellingen/{bestelling.id}"
    return bestelling


@router.put("/{bestelling_id}", response_model=BestellingAntwoord, dependencies=Beheerder)
def wijzig_bestelling(bestelling_id: BestellingId, invoer: BestellingWijziging, sessie: Sessie):
    bestelling = haal_bestelling(sessie, bestelling_id, vergrendel=True)
    for veld, waarde in invoer.model_dump(exclude={"regels"}).items():
        setattr(bestelling, veld, waarde)
    if invoer.regels is not None:
        vervang_regels(bestelling, invoer.regels)
    bestelling.bijgewerkt_op = datetime.now(UTC)
    sessie.commit()
    return bestelling


@router.put("/{bestelling_id}/regels", response_model=list[BestelregelGegevens], dependencies=Beheerder)
def wijzig_bestelregels(
    bestelling_id: BestellingId,
    regels: Annotated[list[BestelregelGegevens], Field(max_length=1000)],
    sessie: Sessie,
):
    bestelling = haal_bestelling(sessie, bestelling_id, vergrendel=True)
    vervang_regels(bestelling, regels)
    bestelling.bijgewerkt_op = datetime.now(UTC)
    sessie.commit()
    return bestelling.regels


@router.delete("/{bestelling_id}", dependencies=Beheerder)
def verwijder_bestelling(bestelling_id: BestellingId, sessie: Sessie):
    bestelling = haal_bestelling(sessie, bestelling_id, vergrendel=True)
    sessie.delete(bestelling)
    sessie.commit()
    return Response(status_code=200)
