# Copilot / AI Agent Instructions for myfavorite

## Quick summary 🔧
- Purpose: Scrape your Toutiao "favorites" to newline-delimited JSON files, download article HTML, convert to Markdown and index to Elasticsearch for searching via a small Flask API + a separate frontend.
- Main components: `toutiao/increasmentdownload.py` -> `toutiao/files/myfavorites-*` (raw JSON pages)
  - `toutiao/html_downloader_requests.py` -> `toutiao/files/htmlcontent-*` (raw HTML per id)
  - `toutiao/esimporter.py` and `toutiao/esimporter_html.py` import/update Elasticsearch indices (`mytoutiaofav`, `mytoutiaofav_html`)
  - `toutiao/apiservice.py` serves search/delete endpoints for the frontend (`views/`, or external `my-search` app started by `start-web.bat`).

## How data flows (big picture) ➡️
1. `increasementdownload.increasement_download()` reads a `curl` template (`curl_cmd.txt`) and writes JSON pages into `toutiao/files/` as `myfavorites-YYYYMMDD-HHMMSS-*.txt` (newline JSON per page).
2. `html_downloader_requests.download_htmls()` reads those `myfavorites-*` files to extract article URLs and writes the HTML to `htmlcontent-myfavorites-*.txt` as JSON lines keyed by id.
3. `ESImporter.import_to_db()` reads `myfavorites-*` (reverse order) and bulk indexes documents into Elasticsearch (`mytoutiaofav`).
4. `ESImporterFromHTMLContent.import_to_db()` converts HTML -> markdown via `converter.convert_html_to_markdown()` and updates docs' `md_content` fields.
5. `apiservice` exposes `/search` and `/remove` for the frontend.

## Key files to examine / edit 📁
- Fetchers / pipeline: `toutiao/increasmentdownload.py`, `toutiao/fulldownload.py`, `toutiao/html_downloader_requests.py`
- Importers/search: `toutiao/esimporter.py`, `toutiao/esimporter_html.py`, `toutiao/essearcher.py`, `toutiao/es.py`
- Web/API: `toutiao/apiservice.py`, `views/myfavs.html`
- Helpers: `toutiao/converter.py`, `toutiao/dbimporter.py`, `toutiao/fulldownload.py`
- Dev-scripts: `toutiao/start-api.bat`, `toutiao/start-es.bat`, `toutiao/start-web.bat`

## Running & common developer workflows ▶️
- Run the full pipeline locally (all components):
  - Start ElasticSearch using `toutiao/start-es.bat` (project expects ES v8.x by the provided script). 
  - Start Flask API: `toutiao/start-api.bat` (runs `apiservice.py`).
  - Start front-end dev server (outside this repo) with `toutiao/start-web.bat`. 
  - Run the backend fetch+import loop: `python toutiao/main_flow.py` (or `python -m toutiao.main_flow`) — this will start background services and the 10-minute fetch loop.
- Run component-only:
  - Collect favorites: `python toutiao/increasmentdownload.py` (writes `myfavorites-*`).
  - Download HTMLs: `python toutiao/html_downloader_requests.py` (writes `htmlcontent-*`).
  - Import JSON to ES: `python toutiao/esimporter.py` or `python toutiao/esimporter_html.py`.
- Tests: `pytest` (tests are under `test/toutiao/*` and use `pytest` + `unittest.mock`).
- Docker: `docker build -t myfavorite .` — Dockerfile installs `requirements.txt` and runs `toutiao/main_flow.py`. Note: the Dockerfile does not run Elasticsearch; you must provide ES accessible at `http://localhost:9200` (or change `ES` URL).

## Project-specific conventions & patterns ⚙️
- Data stored as JSON lines in `toutiao/files/`. Files have strict prefixes: `myfavorites-YYYY*.txt` and `htmlcontent-myfavorites-*.txt`.
- Importers read files in reverse order and use `_locate_position(files, last_id)` to resume from last-indexed ID (see `DBImporter._locate_position`). Tests depend on this behavior — keep the semantics intact.x naming: uses `mytoutiaofav` for main documents and `mytoutiaofav_html` for raw html imports.
- Incremental ordering: ES documents include `increasement_id` assigned by importers to preserve an ordering across imports.
- Networking: `fulldownload.read_curl()` parses `curl_cmd.txt` f
- Indeor a template request. That file contains auth cookies and must be refreshed manually when expired.
- Redirect handling: `html_downloader_requests.send_request()` intentionally sets `allow_redirects=False` and follows limited redirects manually (max 10) — tests and existing logic rely on this.

## Integration points & external dependencies 🔗
- Elasticsearch 8.x locally (script points at a system install path in `start-es.bat`).
- The project relies on a user-provided `curl_cmd.txt` with valid cookies/tokens to access the Toutiao API; if the response becomes empty, suspect token expiration.
- Front-end is a separate repo (`my-search` per `start-web.bat`) that calls the Flask API at `http://localhost:5000/search`.

## Typical troubleshooting tips 💡
- Empty API responses from `increasementdownload` often mean `curl_cmd.txt` cookie/token expired — refresh it by copying a new curl request and replacing the file.
- If ES imports fail, ensure ES is reachable at `http://localhost:9200` and index settings allow writes; check `esimporter.py` error logs and the helper `helpers.bulk` batch sizes.
- For debugging locally, run modules individually (e.g., `python toutiao/essearcher.py`) to isolate failures.

## What an AI agent should do first 🧭
- Locate `curl_cmd.txt` and validate it's present and up-to-date before scripting fetches.
- Prefer small, idempotent changes: add tests for `_locate_position` edge cases or add logging where state is ambiguous.
- When modifying import logic, ensure tests in `test/toutiao/` continue to pass and add tests that capture change in _locate_position behavior or file parsing.

---

If you'd like, I can open a PR with this file and add a short checklist (`ISSUE_TEMPLATE` or `README` section) for onboarding new contributors. Any part you want expanded or clarified? ✅