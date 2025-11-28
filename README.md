# Inventarverwaltung — FastAPI + PostgreSQL + Vue.js

Moderne Full-Stack-Webanwendung zur Verwaltung von Inventargegenständen mit FastAPI-Backend, PostgreSQL-Datenbank und Vue.js-Frontend.

## Überblick

Dieses Projekt ist eine containerisierte Inventarverwaltungsanwendung mit folgenden Komponenten:

- **Backend**: FastAPI (Python) REST-API
- **Frontend**: Vue.js mit Vite
- **Datenbank**: PostgreSQL
- **Orchestrierung**: Docker Compose

Alle Dienste laufen in separaten Docker-Containern und kommunizieren über ein gemeinsames Netzwerk.

## Architektur

### Netzwerk-Kommunikationsstruktur

```
┌──────────────────────────────────────────────────────────────────────┐
│                          Docker Host                                  │
│                                                                       │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │                     Docker Network (Bridge)                    │  │
│  │                                                                │  │
│  │  ┌───────────────┐         ┌───────────────┐         ┌──────────────┐  │
│  │  │   Frontend    │         │    Backend    │         │  PostgreSQL  │  │
│  │  │   Container   │         │   Container   │         │  Container   │  │
│  │  │               │         │               │         │              │  │
│  │  │   Vue.js 3    │  HTTP   │   FastAPI     │  TCP    │  PostgreSQL  │  │
│  │  │   + Vite      │ ──────> │   (uvicorn)   │ ──────> │      15      │  │
│  │  │               │         │               │         │              │  │
│  │  │  Port: 5173   │         │  Port: 8000   │         │  Port: 5432  │  │
│  │  └───────┬───────┘         └───────┬───────┘         └──────┬───────┘  │
│  │          │                         │                         │          │
│  └──────────┼─────────────────────────┼─────────────────────────┼──────────┘
│             │                         │                         │          │
│             │ Port-Mapping            │ Port-Mapping            │ Port-Mapping
│             │ 5173:5173               │ 8000:8000               │ 54320:5432
│             ▼                         ▼                         ▼          │
└─────────────────────────────────────────────────────────────────────────────┘
              │                         │                         │
              │                         │                         │
              ▼                         ▼                         ▼
         Browser                    API Client              PostgreSQL Client
     (localhost:5173)            (localhost:8000)          (localhost:54320)
```

### Kommunikationsprotokolle

**Frontend → Backend (HTTP/REST)**
- Protokoll: HTTP/1.1
- Format: JSON
- Methoden: GET, POST, PUT, DELETE
- Endpunkte: `/items`, `/items/{id}`, `/health`
- CORS: Aktiviert für lokale Entwicklung

**Backend → Datenbank (PostgreSQL-Protokoll)**
- Protokoll: PostgreSQL Wire Protocol (TCP/IP)
- Port: 5432 (intern im Docker-Netzwerk)
- Verbindung: `postgresql://postgres:postgres@db:5432/postgres`
- ORM: SQLModel (basierend auf SQLAlchemy)

### Docker-Netzwerk-Details

- **Netzwerk-Name**: Standard Bridge-Netzwerk (automatisch erstellt)
- **DNS-Auflösung**: Container können sich über Service-Namen erreichen
  - Frontend erreicht Backend über: `http://backend:8000`
  - Backend erreicht Datenbank über: `db:5432`
- **Isolation**: Alle Container laufen im gleichen isolierten Netzwerk

### Datenfluss

1. **Benutzer-Aktion** (Browser)
   - Benutzer öffnet `http://localhost:5173` im Browser
   
2. **Frontend-Request** (Vue.js → FastAPI)
   - Frontend sendet HTTP-Request an `http://localhost:8000/items`
   - Request enthält JSON-Daten (bei POST/PUT)
   
3. **Backend-Verarbeitung** (FastAPI)
   - Empfängt Request und validiert Daten
   - Führt Geschäftslogik aus
   
4. **Datenbank-Abfrage** (FastAPI → PostgreSQL)
   - Backend erstellt SQL-Query über SQLModel
   - Sendet Query an `db:5432`
   
5. **Datenbank-Antwort** (PostgreSQL → FastAPI)
   - PostgreSQL verarbeitet Query
   - Gibt Ergebnis zurück
   
6. **API-Response** (FastAPI → Vue.js)
   - Backend serialisiert Daten zu JSON
   - Sendet HTTP-Response zurück
   
7. **UI-Update** (Vue.js)
   - Frontend empfängt JSON-Daten
   - Aktualisiert die Benutzeroberfläche

### Komponenten

- **Backend (FastAPI)**: REST-API auf Port 8000
- **Frontend (Vue.js)**: Modernes UI mit Splash-Screen, animiertem Hintergrund und Kategorie-Management auf Port 5173
- **PostgreSQL**: Datenbank auf internem Port 5432 (Host: 54320)

## Features

### Frontend
- 🎨 **Animierter Splash-Screen** beim Laden der Anwendung
- 🖼️ **Dekorativer Rahmen** mit Glow-Effekt
- 📁 **Kategorie-Dropdown** mit Option "Neue Kategorie hinzufügen"
- 💾 **Persistente Kategorien** (localStorage)
- ✨ **Moderne Animationen** und Hover-Effekte
- 📱 **Responsive Design** für alle Bildschirmgrößen

### Backend
- ⚡ **FastAPI** für schnelle REST-API
- 🔒 **SQLModel** für typsichere Datenbankoperationen
- 🐘 **PostgreSQL** für zuverlässige Datenspeicherung
- 📝 **Automatische API-Dokumentation** (Swagger UI)

## Datenmodell

Die Anwendung arbeitet mit der Entität `InventoryItem`:

| Feld          | Typ       | Beschreibung                    |
|---------------|-----------|----------------------------------|
| `id`          | Integer   | Primärschlüssel (Auto-Increment)|
| `name`        | String    | Name des Artikels               |
| `category`    | String    | Kategorie (z.B. Hardware)       |
| `status`      | String    | Status (verfügbar/in Verwendung/Wartung) |
| `location`    | String    | Lagerort (z.B. Regal A3)        |
| `assigned_to` | String    | Zugewiesene Person              |

## REST-API Endpunkte

Die API bietet vollständige CRUD-Funktionalität für Inventargegenstände:

### GET /health
Health-Check Endpunkt zur Überprüfung der API-Verfügbarkeit.

**Response:**
```json
{
  "status": "ok"
}
```

---

### GET /items
Alle Inventargegenstände abrufen (mit optionalem Filter).

**Query Parameter:**
- `location` (optional): Filtert nach Lagerort

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "name": "Laptop Dell XPS",
    "description": "15 Zoll, 16GB RAM",
    "quantity": 5,
    "location": "Regal A3",
    "created_at": "2025-11-18T10:30:00"
  }
]
```

**Beispiel:**
```bash
curl http://localhost:8000/items
curl http://localhost:8000/items?location=Regal%20A3
```

---

### GET /items/{item_id}
Einzelnen Inventargegenstand abrufen.

**Path Parameter:**
- `item_id`: ID des Inventargegenstands

**Response:** `200 OK`
```json
{
  "id": 1,
  "name": "Laptop Dell XPS",
  "description": "15 Zoll, 16GB RAM",
  "quantity": 5,
  "location": "Regal A3",
  "created_at": "2025-11-18T10:30:00"
}
```

**Fehler:** `404 Not Found` - Wenn Item nicht existiert

**Beispiel:**
```bash
curl http://localhost:8000/items/1
```

---

### POST /items
Neuen Inventargegenstand anlegen.

**Request Body:**
```json
{
  "name": "Laptop Dell XPS",
  "description": "15 Zoll, 16GB RAM",
  "quantity": 5,
  "location": "Regal A3"
}
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "name": "Laptop Dell XPS",
  "description": "15 Zoll, 16GB RAM",
  "quantity": 5,
  "location": "Regal A3",
  "created_at": "2025-11-18T10:30:00"
}
```

**Beispiel:**
```bash
curl -X POST http://localhost:8000/items \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Laptop Dell XPS",
    "description": "15 Zoll, 16GB RAM",
    "quantity": 5,
    "location": "Regal A3"
  }'
```

---

### PUT /items/{item_id}
Inventargegenstand aktualisieren.

**Path Parameter:**
- `item_id`: ID des zu aktualisierenden Items

**Request Body:**
```json
{
  "name": "Laptop Dell XPS",
  "description": "15 Zoll, 32GB RAM",
  "quantity": 3,
  "location": "Regal B1"
}
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "name": "Laptop Dell XPS",
  "description": "15 Zoll, 32GB RAM",
  "quantity": 3,
  "location": "Regal B1",
  "created_at": "2025-11-18T10:30:00"
}
```

**Fehler:** `404 Not Found` - Wenn Item nicht existiert

**Beispiel:**
```bash
curl -X PUT http://localhost:8000/items/1 \
  -H "Content-Type: application/json" \
  -d '{
    "quantity": 3,
    "location": "Regal B1"
  }'
```

---

### DELETE /items/{item_id}
Inventargegenstand löschen.

**Path Parameter:**
- `item_id`: ID des zu löschenden Items

**Response:** `204 No Content` (bei Erfolg)

**Fehler:** `404 Not Found` - Wenn Item nicht existiert

**Beispiel:**
```bash
curl -X DELETE http://localhost:8000/items/1
```

---

## Schnellstart

### Voraussetzungen

- Docker
- Docker Compose

### Installation und Start

1. **Repository klonen**
   ```powershell
   git clone <repository-url>
   cd FastAPI
   ```

2. **Container starten**
   ```powershell
   docker compose up --build
   ```

3. **Anwendung nutzen**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Dokumentation: http://localhost:8000/docs

### Container stoppen

```powershell
docker compose down
```

### Daten löschen (Reset)

```powershell
docker compose down -v
```

### Container wieder starten

```powershell
docker compose up -d
```

## Entwicklung

### Container-Struktur und Kommunikation

Die Anwendung besteht aus drei separaten Docker-Containern, die über ein gemeinsames Docker-Netzwerk miteinander kommunizieren:

#### Container-Übersicht

1. **Frontend-Container (`frontend`)**
   - Basis: Node.js
   - Port: 5173 (Host) → 5173 (Container)
   - Funktion: Vite Development Server für Vue.js
   - Zugriff auf Backend über: `http://localhost:8000`

2. **Backend-Container (`backend`)**
   - Basis: Python 3.11
   - Port: 8000 (Host) → 8000 (Container)
   - Funktion: FastAPI REST-API Server
   - Zugriff auf Datenbank über: `postgresql://postgres:postgres@db:5432/postgres`

3. **Datenbank-Container (`db`)**
   - Basis: PostgreSQL 15
   - Port: 54320 (Host) → 5432 (Container)
   - Funktion: Persistente Datenspeicherung
   - Volume: `pgdata` für dauerhafte Datenspeicherung

#### Netzwerk-Kommunikation

```
┌─────────────────────────────────────────────────────────────┐
│                    Docker Network (default)                 │
│                                                             │
│  ┌──────────────┐         ┌──────────────┐                  │
│  │  Frontend    │ ──HTTP─>│   Backend    │                  │
│  │  Container   │         │   Container  │                  │
│  │              │         │              │                  │
│  │ Vue.js:5173  │         │ FastAPI:8000 │                  │
│  └──────────────┘         └──────┬───────┘                  │
│                                  │                          │
│                                  │ PostgreSQL Protocol      │
│                                  ▼                          │
│                          ┌──────────────┐                   │
│                          │  Database    │                   │
│                          │  Container   │                   │
│                          │              │                   │
│                          │ Postgres:5432│                   │
│                          └──────┬───────┘                   │
│                                 │                           │
│                                 ▼                           │
│                          ┌──────────────┐                   │
│                          │ Docker Volume│                   │
│                          │   'pgdata'   │                   │
│                          └──────────────┘                   │
└─────────────────────────────────────────────────────────────┘

Host Machine Zugriff:
- Frontend:  http://localhost:5173
- Backend:   http://localhost:8000
- Database:  localhost:54320
```

#### Service-Abhängigkeiten

Die Container starten in folgender Reihenfolge:

1. **db** (Datenbank) - startet zuerst
2. **backend** - wartet auf Health-Check der Datenbank
3. **frontend** - wartet auf Backend-Start

Docker Compose verwendet `depends_on` mit Health-Checks:

```yaml
backend:
  depends_on:
    db:
      condition: service_healthy

frontend:
  depends_on:
    - backend
```

#### Interne vs. Externe Kommunikation

**Interne Kommunikation (Container untereinander):**
- Backend → Database: `db:5432` (Container-Name als Hostname)
- Frontend → Backend: `backend:8000` (im Container-Netzwerk)

**Externe Kommunikation (vom Host/Browser):**
- Browser → Frontend: `localhost:5173`
- Browser → Backend: `localhost:8000`
- Datenbank-Tools → Database: `localhost:54320`

### Datenspeicherung

#### Persistente Daten

Die Anwendungsdaten werden in einem Docker Volume gespeichert, das auch nach dem Stoppen der Container erhalten bleibt:

**Volume-Name:** `pgdata`

**Speicherort auf dem Host:**
- Windows: `\\wsl$\docker-desktop-data\data\docker\volumes\fastapi_pgdata\_data`
- Linux: `/var/lib/docker/volumes/fastapi_pgdata/_data`

#### Datenbank-Schema

Die Datenbank wird beim ersten Start automatisch initialisiert:

1. **Initialisierung:** Das SQL-Script `database/init.sql` wird automatisch ausgeführt
2. **Tabellen:** Die Tabelle `inventoryitem` wird erstellt
3. **Daten:** Beispieldaten (falls vorhanden) werden eingefügt

#### Daten-Lifecycle

**1. Erste Ausführung (docker compose up):**
- Container 'db' startet
- Volume 'pgdata' wird erstellt
- init.sql wird ausgeführt
- Datenbank-Schema wird angelegt

**2. Anwendung läuft:**
- Daten werden in PostgreSQL gespeichert
- Volume 'pgdata' speichert alle Änderungen
- Daten bleiben auch bei Container-Neustart erhalten

**3. Container stoppen (docker compose down):**
- Container werden gestoppt und entfernt
- Volume 'pgdata' bleibt erhalten ✓

**4. Container neu starten (docker compose up):**
- Container werden neu erstellt
- Bestehendes Volume wird wieder eingebunden
- Alle Daten sind noch vorhanden ✓

**5. Kompletter Reset (docker compose down -v):**
- Container werden gestoppt und entfernt
- Volume 'pgdata' wird gelöscht ✗
- Alle Daten gehen verloren!

#### Kategorie-Daten (localStorage)

Benutzerdefinierte Kategorien werden im Browser gespeichert:

**Speicherort:** Browser localStorage
**Key:** `categories`
**Format:** JSON-Array (z.B. `["Hardware", "Software", "Möbel", "Zubehör"]`)

**Wichtig:** Diese Daten sind:
- ✓ Browser-spezifisch (pro Benutzer/Browser)
- ✓ Persistent (bleiben nach Browser-Neustart erhalten)
- ✗ Nicht Container-abhängig
- ✗ Nicht in der Datenbank gespeichert

#### Backup und Wiederherstellung

**Datenbank sichern:**
```powershell
docker exec fastapi-db-1 pg_dump -U postgres postgres > backup.sql
```

**Datenbank wiederherstellen:**
```powershell
Get-Content backup.sql | docker exec -i fastapi-db-1 psql -U postgres -d postgres
```

**Volume sichern:**
```powershell
docker run --rm -v fastapi_pgdata:/data -v ${PWD}:/backup alpine tar czf /backup/pgdata-backup.tar.gz -C /data .
```

**Volume wiederherstellen:**
```powershell
docker run --rm -v fastapi_pgdata:/data -v ${PWD}:/backup alpine tar xzf /backup/pgdata-backup.tar.gz -C /data
```

### Projekt-Struktur

- **backend/** - FastAPI Backend
  - **app/** - Anwendungscode
    - `__init__.py`
    - `main.py` - FastAPI App & Endpunkte
    - `models.py` - SQLModel Datenmodelle
    - `crud.py` - Datenbankoperationen
    - `database.py` - DB-Verbindung
    - **static/** - Statische Dateien
      - `index.html`
  - `Dockerfile`
  - `requirements.txt`
- **frontend/** - Vue.js Frontend
  - **src/**
    - `App.vue` - Vue Hauptkomponente
    - `main.js`
  - `Dockerfile`
  - `package.json`
  - `vite.config.js`
- **database/**
  - `init.sql` - DB-Initialisierung
- `docker-compose.yml`

### API-Dokumentation

FastAPI generiert automatisch eine interaktive API-Dokumentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Datenbank-Zugriff

PostgreSQL ist auf dem Host unter Port 54320 erreichbar:

```powershell
# Mit psql verbinden
psql -h localhost -p 54320 -U postgres -d postgres
```