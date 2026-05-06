from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

from scraper_engine.models import ScrapedReport

MILLE_LACS_SOURCE = "Mille Lacs"
MILLE_LACS_URL = "https://millelacs.com/lake-and-fishing-reports"


def _extract_report_date(page_title: str) -> Optional[datetime]:
    """
    Parse heading text like 'Report as of 05/05/26' into UTC datetime.
    """
    normalized = page_title.strip()
    marker = "report as of "
    lower_title = normalized.lower()
    if marker not in lower_title:
        return None

    date_fragment = normalized[lower_title.index(marker) + len(marker) :].strip()
    for fmt in ("%m/%d/%y", "%m/%d/%Y"):
        try:
            parsed = datetime.strptime(date_fragment, fmt)
            return parsed.replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    return None


def scrape_mille_lacs_report(headless: bool = True) -> ScrapedReport:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=headless)
        page = browser.new_page()
        page.goto(MILLE_LACS_URL, wait_until="networkidle")
        html = page.content()
        browser.close()

    soup = BeautifulSoup(html, "html.parser")

    heading = soup.find(["h1", "h2"], string=lambda text: text and "Report as of" in text)
    title = heading.get_text(" ", strip=True) if heading else "Lake + Fishing Reports"

    report_date = _extract_report_date(title)
    if report_date is None:
        report_date = datetime.now(tz=timezone.utc)

    content_blocks: list[str] = []
    main_content = soup.find("main")
    if main_content:
        paragraphs = main_content.find_all("p")
    else:
        paragraphs = soup.find_all("p")

    for paragraph in paragraphs:
        text = paragraph.get_text(" ", strip=True)
        if text:
            content_blocks.append(text)

    if not content_blocks:
        fallback = soup.get_text(" ", strip=True)
        content_blocks = [fallback[:2000]] if fallback else ["No report body found."]

    body = "\n\n".join(content_blocks)

    return ScrapedReport(
        source=MILLE_LACS_SOURCE,
        title=title,
        body=body,
        report_date=report_date,
        source_url=MILLE_LACS_URL,
    )
