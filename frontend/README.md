# Frontend (Phase 3)

This Next.js + Tailwind app renders the unified fishing report feed and supports
source filtering.

## Features implemented

- Fetches reports from `/api/reports` (a Next.js route that proxies to FastAPI)
- Card-based feed UI with:
  - Source
  - Title
  - Timestamp
  - 150-character preview
  - "Read Full Report" link
- Source filter dropdown (`All` + available source names)
- Responsive layout:
  - 1 column on mobile
  - 2 columns on medium screens
  - 3 columns on large screens

## Run locally

From repository root, start backend first:

```bash
python3 -m uvicorn scraper_engine.api:app --host 127.0.0.1 --port 8000
```

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

## Environment variable (optional)

By default, the frontend proxy route calls:

```text
http://127.0.0.1:8000/api/reports
```

To change it, set:

```text
BACKEND_API_URL
```
