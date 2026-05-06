# Bite-Radar---CastIQ

Minnesota Fishing Reports Aggregator MVP.

Implemented phases:
- Phase 1: Python scraper engine (Mille Lacs source)
- Phase 2: FastAPI backend endpoint (`/api/reports`)
- Phase 3: Next.js + Tailwind frontend feed with source filtering

## Project structure

```text
.
├── .cursor/
│   └── environment.json
├── data/
├── frontend/
├── requirements.txt
└── scraper_engine/
    ├── api.py
    ├── database.py
    ├── main.py
    ├── models.py
    └── scrapers/
        └── mille_lacs.py
```

## Setup (backend)

Run from repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python -m playwright install chromium
```

## Phase 1: scraper

```bash
python -m scraper_engine.main
```

## Phase 2: API

```bash
python -m uvicorn scraper_engine.api:app --host 127.0.0.1 --port 8000 --reload
```

Test API directly:

```bash
curl "http://127.0.0.1:8000/api/reports"
```

## Phase 3: frontend

In a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open:

```text
http://127.0.0.1:3000
```

The frontend calls its own Next.js route (`/api/reports`), which proxies to the
Python backend (`http://127.0.0.1:8000/api/reports` by default).

To point the frontend proxy at a different backend URL:

```bash
cd frontend
BACKEND_API_URL="http://127.0.0.1:8000" npm run dev
```