# Inventarverwaltung — FastAPI + PostgreSQL + Vue.js

Moderne Full-Stack-Webanwendung zur Verwaltung von Inventargegenständen mit FastAPI-Backend, PostgreSQL-Datenbank und Vue.js-Frontend.

## Überblick

Dieses Projekt ist eine containerisierte Inventarverwaltungsanwendung mit folgenden Komponenten:

- **Backend**: FastAPI (Python) REST-API
- **Frontend**: Vue.js 3 mit Vite
- **Datenbank**: PostgreSQL 15
- **Orchestrierung**: Docker Compose

Alle Dienste laufen in separaten Docker-Containern und kommunizieren über ein gemeinsames Netzwerk.

## Architektur

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│  Frontend   │ ───> │   Backend   │ ───> │  PostgreSQL │
│  (Vue.js)   │      │  (FastAPI)  │      │   Database  │
│  Port 5173  │      │  Port 8000  │      │  Port 5432  │
└─────────────┘      └─────────────┘      └─────────────┘
```

### Komponenten

- **Backend (FastAPI)**: REST-API auf Port 8000
- **Frontend (Vue.js)**: Entwicklungsserver auf Port 5173
- **PostgreSQL**: Datenbank auf internem Port 5432 (Host: 5433)

## Datenmodell

Die Anwendung arbeitet mit der Entität `InventoryItem`:

| Feld          | Typ       | Beschreibung                    |
|---------------|-----------|----------------------------------|
| `id`          | Integer   | Primärschlüssel (Auto-Increment)|
| `name`        | String    | Name des Artikels               |
| `description` | String    | Optionale Beschreibung          |
| `quantity`    | Integer   | Verfügbare Menge                |
| `location`    | String    | Lagerort (z.B. Regalfach)       |
| `created_at`  | Timestamp | Erstellungszeitpunkt            |

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

## Entwicklung

### Projekt-Struktur

```
FastAPI/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py          # FastAPI App & Endpunkte
│   │   ├── models.py        # SQLModel Datenmodelle
│   │   ├── crud.py          # Datenbankoperationen
│   │   ├── database.py      # DB-Verbindung
│   │   └── static/
│   │       └── index.html   # Statisches HTML
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.vue          # Vue Hauptkomponente
│   │   └── main.js
│   ├── Dockerfile
│   ├── package.json
│   └── vite.config.js
├── database/
│   └── init.sql             # DB-Initialisierung
└── docker-compose.yml
```

### API-Dokumentation

FastAPI generiert automatisch eine interaktive API-Dokumentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Datenbank-Zugriff

PostgreSQL ist auf dem Host unter Port 5433 erreichbar:

```powershell
# Mit psql verbinden
psql -h localhost -p 5433 -U postgres -d postgres
```