# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 1. Project Overview

Spendly — a personal expense tracker web app (amounts in ₹), built as a step-by-step learning project. Server-rendered Flask app with no front-end framework and no ORM. Most of the app is scaffolding: a handful of pages are fully built, and the rest are placeholder routes marked with step comments for students to implement.

## 2. Architecture

Request flow: browser → route in `app.py` → `render_template()` → Jinja2 renders the page against `base.html` → static CSS/JS fetched separately by the browser. Once `database/db.py` is implemented, routes will call into it for reads/writes against SQLite.

- **`app.py`** — the entire Flask app: every route lives here in one file, no blueprints.
- **`main.py`** — leftover `uv init` template file, unused by the app. Not the entry point.
- **`database/db.py`** — intended to hold `get_db()`, `init_db()`, `seed_db()` for SQLite access via the stdlib `sqlite3` module (no ORM). Currently just a comment describing the contract.
- **`templates/`** — Jinja2 templates. `base.html` is the shared layout (head/fonts/navbar/footer); every page template extends it.
- **`static/css/style.css`** — all styling, driven by CSS custom properties defined in `:root`.
- **`static/js/main.js`** — vanilla JS, added incrementally per feature.

## 3. Where Things Belong

- New routes/view functions → `app.py`.
- New SQL/data-access logic → `database/db.py`, called from routes (not written inline in `app.py`).
- New pages → a template in `templates/` that extends `base.html`; add the route in `app.py` to render it.
- Shared layout changes (nav, footer, fonts, head) → `templates/base.html`, not individual pages.
- New styling → `static/css/style.css`, reusing existing CSS variables (colors, fonts, radii) from `:root` rather than hardcoding new values.
- New client-side behavior → `static/js/main.js`, scoped to the feature it supports (see the existing modal code for the pattern: grab elements, bail if absent, attach listeners in an IIFE).
- `requirements.txt` and `pyproject.toml`/`uv.lock` must stay in sync — add dependencies via `uv add`, not by hand-editing one file only.

## 4. Code Style

- Templates: `{% extends "base.html" %}`, then `{% block title %}`, `{% block content %}`, `{% block scripts %}` as needed. Use `url_for(...)` for all internal links/static references, never hardcoded paths.
- CSS: class-name-driven (no IDs for styling), BEM-ish component prefixes (e.g. `hero-`, `mock-`, `nav-`), variables for color/spacing/radius defined once in `:root`. Section dividers use the `/* ---- */` banner comment style already in `style.css`.
- JS: plain ES5-style vanilla JS wrapped in an IIFE, `var` (not `let`/`const`), early-return guards when expected elements are missing, comments only to explain *why* a non-obvious timing/ordering choice was made (e.g. forcing reflow, delaying hide for a CSS transition).
- Python: routes are small and declarative — a route calls a template or (once built) a `database/db.py` function and returns; keep business logic out of `app.py` once the database layer exists.

## 5. Tech Constraints

- Python 3.13 (pinned in `.python-version` and `pyproject.toml`).
- Flask 3.1.3 + Werkzeug 3.1.6 — no other web framework.
- SQLite via stdlib `sqlite3` only — no SQLAlchemy or other ORM.
- No front-end framework/build step — plain HTML/CSS/JS served by Flask's default `templates/`/`static/` conventions, so those folders must stay adjacent to `app.py`.
- `uv` manages the environment (`pyproject.toml` + `uv.lock`); there is no system-Python install path for this project.
- `expense_tracker.db` is gitignored and created at runtime — never commit it.

## 6. Commands

Dependencies and the venv are managed with `uv`. Do not run `python` or `pip` directly — the system Python has no packages installed; always go through `uv run`.

- Run the app: `uv run python app.py` (serves on `http://127.0.0.1:5001`, debug mode on — auto-reloads on file changes)
- Install/sync dependencies: `uv sync`
- Add a dependency: `uv add <package>`
- Run tests: `uv run pytest` (pytest and pytest-flask are installed but no test files exist yet)
- Check installed packages: `uv pip list`

There is no persistent shell in this environment, so `.venv\Scripts\Activate.ps1` only lasts for a single command here — prefer `uv run ...` over trying to activate the venv.

## 7. Implemented vs Stub Routes

Implemented (render real templates):
- `/` — landing page
- `/register` — sign-up page (GET only; form POSTs will 405 until the handler is built)
- `/login` — sign-in page (GET only; form POSTs will 405 until the handler is built)
- `/terms` — terms and conditions
- `/privacy` — privacy policy

Stub/placeholder (return a plain string, marked `# Placeholder routes — students will implement these` in `app.py`):
- `/logout`
- `/profile`
- `/expenses/add`
- `/expenses/<int:id>/edit`
- `/expenses/<int:id>/delete`

Also unbuilt: `database/db.py` (`get_db`/`init_db`/`seed_db` are comment-only stubs — no database exists yet).

## 8. Warnings and Things to Avoid

- Don't treat the stub routes' current string-return bodies as intentional behavior to preserve — they're placeholders, not finished features.
- Don't add an ORM (e.g. SQLAlchemy) — the course's intended persistence layer is plain SQL via `sqlite3`.
- Don't introduce a CSS/JS framework or bundler — the project is deliberately framework-free.
- Don't hand-edit only `requirements.txt` or only `pyproject.toml` when adding a dependency — use `uv add` so both and `uv.lock` stay consistent.
- Don't run `python`/`pip` directly in commands — the system interpreter lacks the project's dependencies; always use `uv run`.
- Don't commit `expense_tracker.db` or anything under `.venv/` — both are gitignored for a reason.
- Register/login POST handlers don't exist yet — submitting those forms will currently 405; this is expected until the corresponding step is implemented, not a bug to silently work around.
