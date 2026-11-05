# Spec: Registration

## Overview

Spendly currently has a GET-only `/register` route that renders a static
sign-up form; submitting it 405s because no POST handler exists. This step
wires the existing `register.html` form to the database layer built in the
previous step: validate the submitted name/email/password, hash the
password, insert a new row into `users` via `database/db.py`, and start a
logged-in session so the user lands somewhere useful after signing up. This
is the first step that makes "logged in" a real concept in the app, which
later steps (profile, expense CRUD) will depend on.

## Depends on

- Database setup (`database/db.py` — `get_db`, `init_db`, `users` table)
  is already implemented and must not be modified.

## Routes

- `POST /register` — validate input, create the user, log them in,
  redirect to `/profile` — public
- `GET /logout` — clear the session, redirect to `/login` — logged-in
  (needed so a registered/logged-in session can be exited to retest;
  replaces the current placeholder string response)

If no new routes beyond this: none — `GET /register` already exists and
is unchanged.

## Database changes

No schema changes. `users` table already has `id`, `name`, `email`,
`password_hash`, `created_at` (see `database/db.py`). This step adds a new
function to `database/db.py`:

- `create_user(name, email, password_hash)` — parameterized `INSERT` into
  `users`, returns the new user's id. Must let the caller catch
  `sqlite3.IntegrityError` for duplicate email (`UNIQUE` constraint) rather
  than swallowing it.
- `get_user_by_email(email)` — parameterized `SELECT`, used to pre-check
  for a duplicate email and produce a friendly error message instead of a
  raw integrity-error page.

## Templates

- **Create:** none — `templates/register.html` already has the form
  posting to `/register` and already renders `{{ error }}`.
- **Modify:** none required. If validation errors need per-field detail,
  `register.html` may be extended to redisplay the submitted `name`/`email`
  values, but this is optional polish, not required for done.

## Files to change

- `app.py` — add the `/register` POST handler (reusing the existing
  `@app.route("/register")` by allowing `methods=["GET", "POST"]`), and
  replace the placeholder `/logout` route with a real session-clearing
  implementation.
- `database/db.py` — add `create_user` and `get_user_by_email`.

## Files to create

- None.

## New dependencies

No new dependencies. `werkzeug.security` (already used in `seed_db`) is
reused for `generate_password_hash`; Flask's built-in `session` is reused
for login state (requires `app.secret_key`, see rules below).

## Rules for implementation

- No SQLAlchemy or ORMs.
- Parameterised queries only.
- Passwords hashed with `werkzeug.security.generate_password_hash`; never
  store or log plaintext passwords.
- `app.secret_key` must be set (e.g. from `os.urandom` or a fixed dev
  value) for `session` to work — add this once near `app = Flask(__name__)`.
- Validate on the server even though the HTML form has `required`/`type`
  attributes: non-empty name, plausible email format, password length
  >= 8 characters. On failure, re-render `register.html` with `error` set
  and an appropriate HTTP status (400), not a redirect.
- Duplicate email must show a friendly `error` message on the same page
  ("An account with this email already exists."), not a raw SQLite
  traceback.
- Use CSS variables — never hardcode hex values (only relevant if
  `register.html`/`style.css` are touched for error-state styling).
- All templates extend `base.html`.
- Keep `app.py` routes small and declarative — validation/hashing glue can
  live in the route, but all SQL goes through `database/db.py`.

## Definition of done

- [ ] `uv run python app.py` starts without errors.
- [ ] Submitting `/register` with a new name/email/password creates a row
      in the `users` table with a hashed (not plaintext) password.
- [ ] After successful registration, the browser is redirected to
      `/profile` and the session is logged in (no re-login required).
- [ ] Submitting `/register` with an email that already exists in `users`
      (e.g. `demo@spendly.com`) re-renders `register.html` with a friendly
      error and does not insert a duplicate row.
- [ ] Submitting `/register` with a password under 8 characters, or a
      missing name/email, re-renders `register.html` with an error and
      does not touch the database.
- [ ] Visiting `/logout` after registering clears the session and
      redirects to `/login`.
- [ ] `GET /register` still renders the existing form unchanged.
