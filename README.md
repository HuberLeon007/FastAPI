# Inventarverwaltung — FastAPI + PostgreSQL + Docker

Dieses Repository enthält ein Lehrprojekt zur Umsetzung einer kleinen Inventarverwaltungs-
anwendung mit einem FastAPI-Backend, einer PostgreSQL-Datenbank und einer einfachen Webober-
fläche (statische HTML/JavaScript oder kleines SPA). Das Projekt ist so ausgelegt, dass es lo-
kal in Containern läuft und reproduzierbar gestartet werden kann.

## Ziel

Ziel ist eine einfache Inventarverwaltung (Inventarverwaltung / Lagerverwaltung) mit CRUD-
Funktionalität für Inventarposten. Die Anwendung besteht aus zwei Containern:

- Backend-Container (FastAPI) — erreichbar auf Port 8000
- PostgreSQL-Container — interner Port 5432, auf dem Host wird Port 5433 freigegeben

Das Backend liefert die statischen Frontend-Dateien aus (Standardfall). Alternativ kann ein se-
parates Frontend verwendet werden, wenn dies begründet wird.

## Architekturüberblick

- FastAPI (Python) als REST-API
- PostgreSQL als persistenter Datenspeicher (Volume für persistente Daten)
- Docker Compose zur Orchestrierung der beiden Container im gemeinsamen Netzwerk

## Datenmodell

Wir verwenden eine einzelne Entität `InventoryItem` für das Inventar mit folgenden Attributen:

- id: integer, Primärschlüssel (autoincrement)
- name: string, Name des Artikels
- description: string, optionale Beschreibung
- quantity: integer, verfügbare Menge
- location: string, Lagerort (z. B. Regalfach)
- created_at: timestamp, Erstellungszeitpunkt

ER in Worten: InventoryItem(id, name, description, quantity, location, created_at)

## REST-Endpunkte (erste Fassung)

- GET  /items               — Liste aller Inventarposten (optional: filter by location)
- POST /items               — Neuen Inventarposten anlegen
- GET  /items/{id}          — Details eines Postens
- PUT  /items/{id}          — Posten aktualisieren
- DELETE /items/{id}        — Posten löschen

Die API wird JSON verwenden und einfache Validierung über Pydantic-Schemas durchführen.

## Container- und Port-Konfiguration

- PostgreSQL-Container:
  - interner Port: 5432
  - auf Host gebundener Port: 5433
  - Persistenter Datenordner: Docker Volume (z. B. `pgdata`)
- Backend-Container (FastAPI):
  - Port 8000 (uvicorn)
  - Liefert statische Dateien (Frontend) aus `backend/app/static` oder `backend/app/frontend_dist`

Ein `docker-compose.yml` wird beide Dienste im selben Netzwerk starten und ein Volume für die
DB bereitstellen.

## Erste Implementierungsschritte (Kurzfassung / To-Do)

Die folgenden Schritte sind die nächsten konkreten Aufgaben, die wir nacheinander umsetzen wer-
den. Jede Aufgabe ist klein genug, um danach getestet zu werden.

1. Backend-Skelett erstellen
	- Verzeichnis: `backend/app`
	- Dateien: `main.py`, `models.py`, `schemas.py`, `crud.py`, `database.py`, `static/` für das Frontend
	- Einfachen FastAPI-Server starten, der auf `/health` mit 200 antwortet

2. Dockerfile für das Backend
	- Basisimage: `python:3.14-slim` (oder neuer)
	- Installation der Anforderungen (fastapi, uvicorn, sqlalchemy/asyncpg oder psycopg2)

3. `docker-compose.yml` hinzufügen
	- Dienste: `db` (postgres:15 oder neuer) und `backend`
	- Ports: `5433:5432` für db, `8000:8000` für backend
	- Volume für PostgreSQL-Daten

4. Datenbankmodell und Verbindung
	- Modell `InventoryItem` anlegen (SQLAlchemy oder SQLModel)
	- DB-Verbindungsstring über Umgebungsvariable (z. B. `DATABASE_URL`)
	- In Dev: `create_all()` oder einfache Migration einrichten (Alembic optional)

5. CRUD-Endpunkte implementieren
	- Endpunkte gemäß Spezifikation
	- Pydantic-Schemas für Request/Response
	- Grundlegende Fehlerbehandlung (404, 400)

6. Einfaches Frontend
	- `backend/app/static/index.html` mit JavaScript, das die API nutzt
	- Anzeige, Filter, Formular zum Anlegen / Bearbeiten

7. Tests
	- `pytest`-Tests für die API-Endpunkte (happy path + 1-2 Randfälle)

8. Dokumentation
	- Prompts und wichtige AI-Antworten dokumentieren
	- Benutzer- und Entwickleranleitung in `README.md`

## Wie man lokal startet (Schnellstart)

Voraussetzungen: Docker und Docker Compose installiert.

Im PowerShell (Windows) im Projektverzeichnis:

```powershell
# Environment-Datei kopieren (falls vorhanden)
Copy-Item .env.sample .env -ErrorAction SilentlyContinue

# Container bauen und starten
docker compose up --build

# Backend ist dann unter http://localhost:8000 erreichbar
# PostgreSQL ist auf dem Host unter Port 5433 erreichbar (z. B. psql -h localhost -p 5433)
```

Die ersten Implementierungsschritte (Backend-Skelett + docker-compose) werden wir als nächstes
einrichten. Nach dem Starten mit `docker compose up --build` sollte der `/health`-Endpoint 200
zurückgeben.

## Umgebungsvariablen (Beispiel)

- DATABASE_URL=postgresql://postgres:postgres@db:5432/postgres
- POSTGRES_USER=postgres
- POSTGRES_PASSWORD=postgres
- POSTGRES_DB=postgres

Hinweis: In `docker-compose.yml` werden die DB-Variablen gesetzt; lokal zum Testen kann eine
.env-Datei benutzt werden.

## Nächste konkrete Schritte (geplante Reihenfolge)

1. Ich erstelle das Backend-Skelett (`backend/app`) mit `main.py` und einem `/health`-Endpoint.
2. Ich schreibe eine einfache `docker-compose.yml` und eine `Dockerfile` für das Backend.
3. Ich implementiere das `InventoryItem`-Modell und einfache CRUD-Endpunkte.
4. Ich fülle ein minimales statisches Frontend in `backend/app/static`.
5. Tests: `pytest`-Suiten für die Endpunkte.

Wenn du einverstanden bist, beginne ich sofort mit Schritt 1 (Backend-Skelett + /health-Endpoint)
und Schritt 2 (Dockerfile + docker-compose). Soll ich das jetzt anlegen?

## Lizenz und Hinweise

Dieses Projekt ist als Lehrprojekt gedacht. Bei Nutzung der KI sind alle Ergebnisse fachlich zu
prüfen. Wichtige Prompts und Antworten sollten dokumentiert und bei Abgabe als Anhang beigelegt
werden.

---

Dateien/Orte, an denen wir als nächstes Änderungen vornehmen werden:

- `backend/app/main.py`  — FastAPI-Entrypoint
- `backend/Dockerfile`   — Dockerfile für Backend
- `docker-compose.yml`   — Compose-Datei im Projekt-Root
- `backend/app/models.py` / `schemas.py` / `crud.py` — DB-Modelle und Logik

# FastAPI