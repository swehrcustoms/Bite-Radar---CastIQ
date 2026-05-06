# Bite-Radar---CastIQ

Phases 1 and 2 of the Minnesota Fishing Reports Aggregator MVP are implemented:
- Phase 1: Python scraper engine
- Phase 2: FastAPI endpoint serving the SQLite data

## Implemented scope

- SQLite database initialization (`data/reports.db`)
- Scraper for first source: **Mille Lacs** (`https://millelacs.com/lake-and-fishing-reports`)
- CLI runner to execute the scrape and persist results
- FastAPI endpoint: `GET /api/reports` sorted by report date (newest first)

## Project structure

```text
.
├── data/
├── requirements.txt
└── scraper_engine/
    ├── api.py
    ├── __init__.py
    ├── database.py
    ├── main.py
    ├── models.py
    └── scrapers/
        └── mille_lacs.py
```

## Local setup (exact commands)

Run these commands from the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python -m playwright install chromium
```

## Phase 1: run scraper

```bash
python -m scraper_engine.main
```

If you want to run with a visible browser window for debugging:

```bash
python -m scraper_engine.main --headed
```

Use a custom database path if needed:

```bash
python -m scraper_engine.main --db-path data/reports.db
```

## Phase 2: run API

```bash
python -m uvicorn scraper_engine.api:app --reload
```

Then open:

```text
http://127.0.0.1:8000/api/reports
```

## What should happen

- A SQLite file is created at `data/reports.db` if it does not already exist.
- The `reports` table is created automatically.
- The latest Mille Lacs report page is scraped.
- One row is inserted (or ignored if duplicate based on source/title/date).
- The API returns JSON sorted by `report_date` descending.