# Spec: Login and Logout

## Overview

Spendly has a GET-only `/login` route that renders a static sign-in form;
submitting it currently 405s because no POST handler exists. `/logout` was
already implemented in the registration step (clears the session and
redirects to `/login`). This step wires the existing `login.html` form to
the database layer: look up the submitted email, verify the password
against the stored hash, and start a logged-in session so the user lands
on `/profile`. This completes the authentication loop (register → login →
logout) that later steps (profile, expense CRUD) depend on for knowing
which user is acting.

## Depends on

- Database setup (`database/db.py` — `get_db`, `init_db`, `users` table)
  is already implemented and must not be modified.
- Registration (`create_user`, `get_user_by_email` in `database/db.py`;
  session-based login pattern established in `POST /register`) is already
  implemented and must not be modified.

## Routes

- `POST /login` — validate credentials, start the session, redirect to
  `/profile` — public
- `GET /logout` — already implemented in the previous step (clears
  session, redirects to `/login`); no change needed here.

## Database changes

No schema changes and no new functions needed. `get_user_by_email(email)`
(added in the registration step) is reused to fetch the stored
`password_hash` for comparison via
`werkzeug.security.check_password_hash`.

If none: No database changes.

## Templates

- **Create:** none — `templates/login.html` already has the form posting
  to `/login` and already renders `{{ error }}`.
- **Modify:** none required.

## Files to change

- `app.py` — change `@app.route("/login")` to
  `@app.route("/login", methods=["GET", "POST"])` and add the POST branch:
  look up the user by email, verify the password with
  `check_password_hash`, set the session on success, redirect to
  `/profile`; on failure, re-render `login.html` with a friendly error and
  a 401 status.

## Files to create

- None.

## New dependencies

No new dependencies. `werkzeug.security.check_password_hash` is reused
(same module `generate_password_hash` already comes from); Flask's
built-in `session` is reused for login state (uses the `app.secret_key`
already set in the registration step).

## Rules for implementation

- No SQLAlchemy or ORMs.
- Parameterised queries only.
- Passwords hashed with werkzeug — verify via
  `werkzeug.security.check_password_hash`, never compare plaintext
  passwords.
- Use CSS variables — never hardcode hex values (only relevant if
  `login.html`/`style.css` are touched for error-state styling).
- All templates extend `base.html`.
- Do not reveal whether the failure was "no such email" or "wrong
  password" — use one generic error message ("Invalid email or
  password.") for both, to avoid leaking which emails are registered.
- Keep `app.py` routes small and declarative — validation/session glue can
  live in the route, but all SQL goes through `database/db.py`.

## Definition of done

- [ ] `uv run python app.py` starts without errors.
- [ ] Submitting `/login` with the seeded demo credentials
      (`demo@spendly.com` / `demo123`) logs the user in and redirects to
      `/profile`.
- [ ] Submitting `/login` with a registered email and the correct
      password logs the user in and redirects to `/profile`.
- [ ] Submitting `/login` with a correct email but wrong password
      re-renders `login.html` with a generic "Invalid email or password."
      error and does not start a session.
- [ ] Submitting `/login` with an email that has no account re-renders
      `login.html` with the same generic error (no indication the email
      doesn't exist).
- [ ] After logging in, visiting `/logout` clears the session and
      redirects to `/login`.
- [ ] `GET /login` still renders the existing form unchanged.
