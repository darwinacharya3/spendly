---
name: flask-saas-ui
description: Build or restyle UI for the user's Flask + vanilla JS project following their house design system (modern SaaS look, indigo accent, light/dark toggle, Inter + monospace, hand-written CSS custom properties, Jinja base/partials, web components). Use whenever the user asks for a page, template, form, dashboard, card, modal, navbar, button, component, or any frontend/HTML/CSS/JS work in their Flask app, even if they don't mention the design system or say "frontend".
---

# Flask SaaS UI

House design system for a Flask app with vanilla JS. The goal is that every page and component looks like it came from one product, so use the tokens and patterns below rather than inventing new colors, sizes or class names. If a request needs something the system doesn't cover, extend it in the same spirit and add the new token to `tokens.css` instead of hard-coding a one-off value.

## Stack rules
- Flask + Jinja templates, hand-written CSS, vanilla JS. No frameworks, no Tailwind, no build step, no CDN UI libraries. Why: the project has no bundler, so anything needing one breaks the setup.
- No inline `style=` attributes or inline `<script>` logic (small `{{ data|tojson }}` bootstrap blobs are fine).
- Use `url_for('static', filename=...)` for every asset.

## File layout
```
static/css/tokens.css      # design tokens (copy from assets/tokens.css)
static/css/base.css        # reset, typography, layout helpers
static/css/components.css  # buttons, cards, forms, tables, badges
static/js/theme.js         # theme toggle
static/js/components/*.js  # one web component per file (ui-modal.js, ui-toast.js ...)
templates/base.html        # layout shell
templates/partials/        # navbar, footer, flash messages
templates/macros/ui.html   # Jinja macros: button, field, card
```
Create missing files from `assets/` when starting a new project; edit existing ones in place otherwise. Pages extend `base.html` and fill `{% block content %}`, with optional `{% block head %}` and `{% block scripts %}`.

## Design tokens (summary)
Full definitions are in `assets/tokens.css`; read `references/design-system.md` for components and usage detail.
- **Style:** modern SaaS: soft shadows, rounded cards, one accent, generous whitespace.
- **Accent:** indigo `#6366f1` (hover `#4f46e5`). Neutrals are slate grays. Semantic colors for success/warning/danger.
- **Type:** Inter for UI text; monospace (JetBrains Mono, fallback `ui-monospace`) for labels, IDs, code, numeric data, and small uppercase eyebrows.
- **Spacing:** 4px base. Use `--space-1` (4px) through `--space-12` only.
- **Radius:** `--radius-md` 8px (inputs, buttons), `--radius-lg` 12px (cards, modals).
- **Shadows:** `--shadow-sm`, `--shadow-md`, `--shadow-lg`, all soft and low-opacity.
- **Themes:** light default; dark via `[data-theme="dark"]` on `<html>`. Components must only reference semantic variables (`--color-bg`, `--color-surface`, `--color-text`, `--color-accent`...), never raw hex, so both themes work automatically.

## CSS conventions
- Plain classes with a short component prefix: `.btn`, `.btn--primary`, `.card`, `.field`, `.badge`. Modifiers use `--`.
- Colors, spacing, radius, shadows, font sizes always come from `var(--token)`.
- Mobile first; breakpoints at 640px and 1024px.
- Visible `:focus-visible` ring using `--color-focus`; respect `prefers-reduced-motion`.

## JavaScript conventions
- Reusable interactive pieces are **web components** (custom elements, prefix `ui-`, e.g. `<ui-modal>`, `<ui-toast>`, `<ui-tabs>`). Define with `customElements.define`, load via `<script type="module">`. Prefer light DOM so global tokens and styles apply; use shadow DOM only when style isolation is truly needed, and then rely on inherited CSS variables.
- One-off page logic goes in a small module under `static/js/pages/`.
- Talk to Flask with `fetch` against JSON routes; handle errors by showing a `<ui-toast>`.
- Theme toggle: `theme.js` sets `data-theme` on `<html>`, persists to `localStorage` (wrapped in try/catch), and defaults to the OS preference. Include a tiny inline-free early script via `theme.js` loaded in `<head>` to avoid a flash of the wrong theme.

## Workflow
1. Check what exists (templates, static files) and match it.
2. Build with tokens and existing components; add a macro or component rather than copy-pasting markup.
3. Verify both themes (check that nothing uses raw colors), keyboard focus, and a narrow viewport.
4. In your summary, list files created/changed and any new tokens added.

## Quality bar
Accessible by default: labels tied to inputs, button vs link used correctly, contrast that holds in both themes, `aria-*` on custom elements (dialog role, `aria-live` for toasts). Keep layouts airy; one primary button per view.---
name: flask-saas-ui
description: Build or restyle UI for the user's Flask + vanilla JS project following their house design system (modern SaaS look, indigo accent, light/dark toggle, Inter + monospace, hand-written CSS custom properties, Jinja base/partials, web components). Use whenever the user asks for a page, template, form, dashboard, card, modal, navbar, button, component, or any frontend/HTML/CSS/JS work in their Flask app, even if they don't mention the design system or say "frontend".
---

# Flask SaaS UI

House design system for a Flask app with vanilla JS. The goal is that every page and component looks like it came from one product, so use the tokens and patterns below rather than inventing new colors, sizes or class names. If a request needs something the system doesn't cover, extend it in the same spirit and add the new token to `tokens.css` instead of hard-coding a one-off value.

## Stack rules
- Flask + Jinja templates, hand-written CSS, vanilla JS. No frameworks, no Tailwind, no build step, no CDN UI libraries. Why: the project has no bundler, so anything needing one breaks the setup.
- No inline `style=` attributes or inline `<script>` logic (small `{{ data|tojson }}` bootstrap blobs are fine).
- Use `url_for('static', filename=...)` for every asset.

## File layout
```
static/css/tokens.css      # design tokens (copy from assets/tokens.css)
static/css/base.css        # reset, typography, layout helpers
static/css/components.css  # buttons, cards, forms, tables, badges
static/js/theme.js         # theme toggle
static/js/components/*.js  # one web component per file (ui-modal.js, ui-toast.js ...)
templates/base.html        # layout shell
templates/partials/        # navbar, footer, flash messages
templates/macros/ui.html   # Jinja macros: button, field, card
```
Create missing files from `assets/` when starting a new project; edit existing ones in place otherwise. Pages extend `base.html` and fill `{% block content %}`, with optional `{% block head %}` and `{% block scripts %}`.

## Design tokens (summary)
Full definitions are in `assets/tokens.css`; read `references/design-system.md` for components and usage detail.
- **Style:** modern SaaS: soft shadows, rounded cards, one accent, generous whitespace.
- **Accent:** indigo `#6366f1` (hover `#4f46e5`). Neutrals are slate grays. Semantic colors for success/warning/danger.
- **Type:** Inter for UI text; monospace (JetBrains Mono, fallback `ui-monospace`) for labels, IDs, code, numeric data, and small uppercase eyebrows.
- **Spacing:** 4px base. Use `--space-1` (4px) through `--space-12` only.
- **Radius:** `--radius-md` 8px (inputs, buttons), `--radius-lg` 12px (cards, modals).
- **Shadows:** `--shadow-sm`, `--shadow-md`, `--shadow-lg`, all soft and low-opacity.
- **Themes:** light default; dark via `[data-theme="dark"]` on `<html>`. Components must only reference semantic variables (`--color-bg`, `--color-surface`, `--color-text`, `--color-accent`...), never raw hex, so both themes work automatically.

## CSS conventions
- Plain classes with a short component prefix: `.btn`, `.btn--primary`, `.card`, `.field`, `.badge`. Modifiers use `--`.
- Colors, spacing, radius, shadows, font sizes always come from `var(--token)`.
- Mobile first; breakpoints at 640px and 1024px.
- Visible `:focus-visible` ring using `--color-focus`; respect `prefers-reduced-motion`.

## JavaScript conventions
- Reusable interactive pieces are **web components** (custom elements, prefix `ui-`, e.g. `<ui-modal>`, `<ui-toast>`, `<ui-tabs>`). Define with `customElements.define`, load via `<script type="module">`. Prefer light DOM so global tokens and styles apply; use shadow DOM only when style isolation is truly needed, and then rely on inherited CSS variables.
- One-off page logic goes in a small module under `static/js/pages/`.
- Talk to Flask with `fetch` against JSON routes; handle errors by showing a `<ui-toast>`.
- Theme toggle: `theme.js` sets `data-theme` on `<html>`, persists to `localStorage` (wrapped in try/catch), and defaults to the OS preference. Include a tiny inline-free early script via `theme.js` loaded in `<head>` to avoid a flash of the wrong theme.

## Workflow
1. Check what exists (templates, static files) and match it.
2. Build with tokens and existing components; add a macro or component rather than copy-pasting markup.
3. Verify both themes (check that nothing uses raw colors), keyboard focus, and a narrow viewport.
4. In your summary, list files created/changed and any new tokens added.

## Quality bar
Accessible by default: labels tied to inputs, button vs link used correctly, contrast that holds in both themes, `aria-*` on custom elements (dialog role, `aria-live` for toasts). Keep layouts airy; one primary button per view.