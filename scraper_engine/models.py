from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class ScrapedReport:
    source: str
    title: str
    body: str
    report_date: datetime
    source_url: str
    scraped_at: datetime | None = None
