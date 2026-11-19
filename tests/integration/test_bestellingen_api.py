import os

import pytest
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url

from cargohub.api import maak_app

PAD = "/api/v1/bestellingen"
GEBRUIKER = {"API_KEY": "test-gebruiker"}
BEHEERDER = {"API_KEY": "test-beheerder"}
BESTELLING = {
    "klant_id": 1, "magazijn_id": 2, "besteldatum": "2026-11-19",
    "regels": [{"artikel_id": "A-1", "aantal": 2, "stukprijs": "1.25"}],
}


@pytest.fixture(scope="module")
def database():
    url = os.getenv("TEST_DATABASE_URL")
    if not url:
        pytest.skip("Stel TEST_DATABASE_URL in voor PostgreSQL-integratietests.")
    assert make_url(url).database == "cargohub_test"
    with pytest.MonkeyPatch.context() as patch:
        patch.setenv("DATABASE_URL", url)
        configuratie = Config("alembic.ini")
        command.upgrade(configuratie, "head")
        command.check(configuratie)
    engine = create_engine(url)
    yield engine
    engine.dispose()


@pytest.fixture
def client(database):
    with database.begin() as verbinding:
        verbinding.execute(text("TRUNCATE bestelling, bestelregel RESTART IDENTITY"))
    app = maak_app(database.url.render_as_string(hide_password=False), *(
        GEBRUIKER["API_KEY"], BEHEERDER["API_KEY"],
    ))
    with TestClient(app) as client:
        yield client
    with database.begin() as verbinding:
        verbinding.execute(text("TRUNCATE bestelling, bestelregel RESTART IDENTITY"))


@pytest.fixture
def geplaatst(client):
    antwoord = client.post(PAD, headers=GEBRUIKER, json=BESTELLING)
    assert antwoord.status_code == 201
    return antwoord.headers["Location"]


def test_bestelling_plaatsen_gebruiker_201(client):
    antwoord = client.post(PAD, headers=GEBRUIKER, json=BESTELLING)
    assert antwoord.status_code == 201
    assert antwoord.json()["status"] == "geplaatst"
    assert antwoord.json()["regels"] == BESTELLING["regels"]


def test_bestellingen_lijst_bevat_geplaatste_bestelling(client, geplaatst):
    assert [item["id"] for item in client.get(PAD, headers=GEBRUIKER).json()] == [
        int(geplaatst.rsplit("/", 1)[1]),
    ]


def test_bestelling_ophalen_bevat_regels(client, geplaatst):
    assert client.get(geplaatst, headers=GEBRUIKER).json()["regels"] == BESTELLING["regels"]


def test_bestelregels_ophalen_bevat_stukprijs(client, geplaatst):
    assert client.get(f"{geplaatst}/regels", headers=GEBRUIKER).json() == BESTELLING["regels"]


def test_bestelling_wijzigen_zonder_regels_behoudt_regels(client, geplaatst):
    invoer = {sleutel: waarde for sleutel, waarde in BESTELLING.items() if sleutel != "regels"}
    antwoord = client.put(geplaatst, headers=BEHEERDER, json={**invoer, "status": "verwerkt"})
    assert antwoord.status_code == 200
    assert antwoord.json()["regels"] == BESTELLING["regels"]


def test_bestelregels_vervangen_slaat_nieuwe_regels_op(client, geplaatst):
    regels = [{"artikel_id": "B-2", "aantal": 5, "stukprijs": None}]
    assert client.put(f"{geplaatst}/regels", headers=BEHEERDER, json=regels).status_code == 200
    assert client.get(f"{geplaatst}/regels", headers=GEBRUIKER).json() == regels


def test_bestelling_verwijderen_verwijdert_regels(client, geplaatst, database):
    assert client.delete(geplaatst, headers=BEHEERDER).status_code == 200
    with database.connect() as verbinding:
        assert verbinding.scalar(text("SELECT count(*) FROM bestelregel")) == 0


@pytest.mark.parametrize(("methode", "achtervoegsel"), [
    ("GET", ""), ("GET", "/regels"), ("PUT", "/regels"), ("DELETE", ""),
])
def test_bestelling_ontbreekt_404(client, methode, achtervoegsel):
    antwoord = client.request(methode, f"{PAD}/999{achtervoegsel}", headers=BEHEERDER, json=[])
    assert antwoord.status_code == 404
