from __future__ import annotations

from pathlib import Path
from typing import Any

from fastapi import FastAPI

from scraper_engine.database import ensure_database, fetch_reports

DEFAULT_DB_PATH = Path("data/reports.db")

app = FastAPI(title="MN Fishing Reports API", version="0.1.0")


@app.get("/api/reports")
def get_reports(db_path: str = str(DEFAULT_DB_PATH)) -> list[dict[str, Any]]:
    """
    Return scraped reports sorted by newest report date first.

    db_path is exposed as a query param to simplify local testing against
    alternate SQLite files while keeping the default at data/reports.db.
    """
    resolved_path = Path(db_path)
    ensure_database(resolved_path)
    return fetch_reports(resolved_path)
