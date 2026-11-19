import pytest
from fastapi.testclient import TestClient

from cargohub.api import maak_app


@pytest.fixture
def client():
    app = maak_app("postgresql+psycopg://localhost/ongebruikt", "test-gebruiker", "test-beheerder")
    with TestClient(app) as client:
        yield client


@pytest.mark.parametrize("sleutel", [None, "onbekend"])
def test_bestellingen_ongeldige_authenticatie_401(client, sleutel):
    headers = {"API_KEY": sleutel} if sleutel else {}
    assert client.get("/api/v1/bestellingen", headers=headers).status_code == 401


@pytest.mark.parametrize(
    ("methode", "pad"),
    [("PUT", "/1"), ("PUT", "/1/regels"), ("DELETE", "/1")],
)
def test_bestellingen_gebruiker_mag_niet_beheren_403(client, methode, pad):
    antwoord = client.request(
        methode, f"/api/v1/bestellingen{pad}", headers={"API_KEY": "test-gebruiker"},
    )
    assert antwoord.status_code == 403


@pytest.mark.parametrize("id", ["geen-getal", "0", "9223372036854775808"])
def test_bestelling_ongeldig_id_400(client, id):
    antwoord = client.get(f"/api/v1/bestellingen/{id}", headers={"API_KEY": "test-gebruiker"})
    assert antwoord.status_code == 400


@pytest.mark.parametrize("regel", [
    {"artikel_id": "A-1", "aantal": 0},
    {"artikel_id": "A-1", "aantal": True},
    {"artikel_id": "A-1", "aantal": 1, "stukprijs": "1.001"},
    {"artikel_id": "A-1", "aantal": 1, "status": "verzonden"},
])
def test_bestelling_ongeldige_regel_400(client, regel):
    antwoord = client.post(
        "/api/v1/bestellingen", headers={"API_KEY": "test-gebruiker"},
        json={"klant_id": 1, "magazijn_id": 2, "besteldatum": "2026-11-19", "regels": [regel]},
    )
    assert antwoord.status_code == 400


def test_bestelling_ongeldige_app_sleutels():
    with pytest.raises(ValueError):
        maak_app("postgresql+psycopg://localhost/ongebruikt", "gelijk", "gelijk")
