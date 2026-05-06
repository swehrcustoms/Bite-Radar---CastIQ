from __future__ import annotations

import argparse
from pathlib import Path

from scraper_engine.database import ensure_database, upsert_reports
from scraper_engine.scrapers.mille_lacs import scrape_mille_lacs_report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run Phase 1 scraper(s) and persist reports to SQLite."
    )
    parser.add_argument(
        "--db-path",
        default="data/reports.db",
        help="Path to the SQLite database file (default: data/reports.db).",
    )
    parser.add_argument(
        "--headed",
        action="store_true",
        help="Run Playwright in headed mode (visible browser) for debugging.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    db_path = Path(args.db_path)
    ensure_database(db_path)

    report = scrape_mille_lacs_report(headless=not args.headed)

    inserted = upsert_reports(db_path, [report])
    print(
        f"Scrape complete. source={report.source} title={report.title!r} "
        f"inserted_rows={inserted} db={db_path}"
    )


if __name__ == "__main__":
    main()
