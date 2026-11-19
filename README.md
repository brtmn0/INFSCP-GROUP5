# CargoHub Bestellingen

Nieuwe API voor bestellingen, gebouwd met FastAPI, SQLAlchemy, psycopg en PostgreSQL.
Gebruik Python 3.11 of hoger. Installeer de ontwikkelafhankelijkheden met
`python -m pip install -r requirements-dev.txt`.

Maak een lege PostgreSQL-database aan. Stel in PowerShell de volgende variabelen in
met de gegevens van je lokale omgeving en kies twee verschillende API-sleutels.

```powershell
$env:DATABASE_URL = 'postgresql+psycopg://<gebruiker>:<wachtwoord>@localhost/cargohub'
$env:CARGOHUB_GEBRUIKERSSLEUTEL = '<gebruikerssleutel>'
$env:CARGOHUB_BEHEERDERSSLEUTEL = '<beheerderssleutel>'
python -m alembic upgrade head
python -m uvicorn cargohub.api:maak_app_uit_omgeving --factory
```

De interactieve API-documentatie staat op `http://127.0.0.1:8000/docs`.
Stuur bij ieder verzoek de header `API_KEY`.

| Methode | Route | Toegang |
|---|---|---|
| GET | `/api/v1/bestellingen` | Gebruiker en beheerder |
| GET | `/api/v1/bestellingen/{bestelling_id}` | Gebruiker en beheerder |
| GET | `/api/v1/bestellingen/{bestelling_id}/regels` | Gebruiker en beheerder |
| POST | `/api/v1/bestellingen` | Gebruiker en beheerder |
| PUT | `/api/v1/bestellingen/{bestelling_id}` | Beheerder |
| PUT | `/api/v1/bestellingen/{bestelling_id}/regels` | Beheerder |
| DELETE | `/api/v1/bestellingen/{bestelling_id}` | Beheerder |

Een voorbeeld voor POST. De API genereert het ID en zet de status op `geplaatst`.

```json
{
  "klant_id": 1,
  "magazijn_id": 2,
  "besteldatum": "2026-11-19",
  "regels": [{"artikel_id": "A-1", "aantal": 2, "stukprijs": "1.25"}]
}
```

PUT op een bestelling vervangt de bestelgegevens en vereist een status. Laat
`regels` weg om de huidige regels te behouden. PUT op `/regels` verwacht een
JSON-lijst en vervangt alle regels. Een lege lijst wist de regels.

Deze eerste versie gebruikt één gedeelde sleutel per rol. Beide rollen mogen
alle bestellingen lezen. Klant-, magazijn- en artikel-ID's zijn externe
verwijzingen. Controle op het bestaan van die gegevens, voorraadreservering en
import van legacygegevens volgen bij de koppeling met de andere onderdelen.

## Testen

```powershell
python -m ruff check .
python -m pytest tests/unit
$env:TEST_DATABASE_URL = 'postgresql+psycopg://<gebruiker>:<wachtwoord>@localhost/cargohub_test'
python -m pytest --cov=cargohub --cov-fail-under=75
```

Maak voor de integratietests een aparte, lege database met de naam
`cargohub_test`. De tests passen de migraties toe en wissen de bestelgegevens
in die testdatabase tussen tests.
