# Spec: Profile Page Design

## Overview

Spendly's `/profile` route currently returns a plain placeholder string
("Profile page — coming in Step 4"). This step replaces it with a real,
logged-in-only profile page that shows the signed-in user's account
details (name, email, member-since date) and a small summary of their
expense activity (total expenses logged, total amount spent). It builds
on the session-based auth established in registration/login and gives
users a landing spot that reflects who they are and how they've used the
app so far, ahead of full expense CRUD (steps 7–9).

## Depends on

- Database setup (`database/db.py` — `get_db`, `init_db`, `users` and
  `expenses` tables) is already implemented and must not be modified.
- Registration (`create_user`, `get_user_by_email`) is already
  implemented and must not be modified.
- Login/Logout (session `user_id`, `current_user` context processor in
  `app.py`) is already implemented and must not be modified.

## Routes

- `GET /profile` — render the profile page with the current user's
  details and expense summary; redirect to `/login` if no session —
  logged-in only

## Database changes

No new tables or columns. One new read-only helper function in
`database/db.py`:

- `get_expense_summary(user_id)` — returns the count of expenses and the
  sum of `amount` for that user (e.g. via a single
  `SELECT COUNT(*), COALESCE(SUM(amount), 0) FROM expenses WHERE user_id = ?`
  query), so the route doesn't write raw SQL inline.

## Templates

- **Create:** `templates/profile.html` — extends `base.html`; shows the
  user's name, email, and "member since" date (formatted from
  `created_at`), plus the expense summary (count and total ₹ spent).
- **Modify:** None. `base.html` nav already links to `/profile` for
  logged-in users (no changes needed there).

## Files to change

- `app.py` — replace the placeholder `/profile` route with the real
  implementation (login check, call `get_expense_summary`, render
  `profile.html`).
- `database/db.py` — add `get_expense_summary(user_id)`.
- `static/css/style.css` — add profile page styling (new rules only,
  reusing existing `:root` variables).

## Files to create

- `templates/profile.html`

## New dependencies

No new dependencies.

## Rules for implementation

- Before writing `profile.html` or the new CSS, consult the
  `frontend-design` skill (house design system: Jinja base/partials,
  indigo accent, Inter + monospace, hand-written CSS custom properties)
  for layout and component choices, rather than improvising a one-off
  look.
- No SQLAlchemy or ORMs.
- Parameterised queries only.
- Passwords hashed with werkzeug (not touched in this step, but existing
  hashing must not be altered).
- Use CSS variables — never hardcode hex values.
- All templates extend `base.html`.
- `/profile` must redirect anonymous visitors to `/login`; don't render
  the page without a session.
- Don't modify `database/db.py` functions outside of adding
  `get_expense_summary`.

## Definition of done

- [ ] Visiting `/profile` while logged out redirects to `/login`.
- [ ] Logging in and visiting `/profile` renders the real page (no plain
      string response).
- [ ] The page shows the logged-in user's name, email, and a correctly
      formatted member-since date.
- [ ] The page shows the correct expense count and total ₹ amount for
      that user (verify against `seed_db()` demo data: 8 expenses).
- [ ] A user with zero expenses sees a sensible empty state (count 0,
      total ₹0) instead of an error.
- [ ] Page styling uses only existing CSS variables from `:root` — no
      hardcoded hex values introduced.
- [ ] `uv run python app.py` runs without errors and `/profile` renders
      correctly in the browser for the seeded demo user.
