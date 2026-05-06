# Bite-Radar---CastIQ

Phase 1 of the Minnesota Fishing Reports Aggregator MVP is implemented here as a
Python scraper engine.

## Phase 1 scope

- SQLite database initialization (`data/reports.db`)
- Scraper for first source: **Mille Lacs** (`https://millelacs.com/lake-and-fishing-reports`)
- CLI runner to execute the scrape and persist results

## Project structure

```text
.
├── data/
├── requirements.txt
└── scraper_engine/
    ├── __init__.py
    ├── database.py
    ├── main.py
    ├── models.py
    └── scrapers/
        └── mille_lacs.py
```

## Local setup and run (exact commands)

Run these commands from the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python -m playwright install chromium
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

## What should happen

- A SQLite file is created at `data/reports.db` if it does not already exist.
- The `reports` table is created automatically.
- The latest Mille Lacs report page is scraped.
- One row is inserted (or ignored if duplicate based on source/title/date).