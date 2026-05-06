"""SQLite initialization and persistence helpers for scraped reports."""

from __future__ import annotations

import sqlite3
from pathlib import Path
from datetime import datetime, timezone
from typing import Iterable

from scraper_engine.models import ScrapedReport


def ensure_database(db_path: Path) -> None:
    """Create the reports table if it does not exist."""
    db_path.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(db_path) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT NOT NULL,
                title TEXT NOT NULL,
                body TEXT NOT NULL,
                report_date TEXT,
                source_url TEXT NOT NULL,
                scraped_at TEXT NOT NULL,
                UNIQUE(source, title, report_date)
            )
            """
        )
        connection.commit()


def initialize_database(db_path: Path) -> None:
    """Backward-compatible alias for database initialization."""
    ensure_database(db_path)


def upsert_reports(db_path: Path, reports: Iterable[ScrapedReport]) -> int:
    """Insert reports while ignoring duplicates using the UNIQUE constraint."""
    rows = []
    for report in reports:
        scraped_at = report.scraped_at or datetime.now(tz=timezone.utc)
        rows.append(
            (
                report.source,
                report.title,
                report.body,
                report.report_date.isoformat(),
                report.source_url,
                scraped_at.isoformat(),
            )
        )
    if not rows:
        return 0

    with sqlite3.connect(db_path) as connection:
        cursor = connection.executemany(
            """
            INSERT OR IGNORE INTO reports (
                source, title, body, report_date, source_url, scraped_at
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            rows,
        )
        connection.commit()
        return cursor.rowcount if cursor.rowcount is not None else 0


def upsert_report(db_path: Path, report: ScrapedReport) -> int:
    """Insert a single report and return the inserted count (0 or 1)."""
    return upsert_reports(db_path, [report])


def fetch_reports(db_path: Path, limit: int | None = None) -> list[dict[str, str | int | None]]:
    """
    Fetch reports sorted by report_date (newest first) then id (newest first).
    """
    query = """
        SELECT id, source, title, body, report_date, source_url, scraped_at
        FROM reports
        ORDER BY
            COALESCE(report_date, scraped_at) DESC,
            id DESC
    """
    params: tuple[int, ...] = ()
    if limit is not None:
        query += " LIMIT ?"
        params = (limit,)

    with sqlite3.connect(db_path) as connection:
        connection.row_factory = sqlite3.Row
        rows = connection.execute(query, params).fetchall()
        return [dict(row) for row in rows]
