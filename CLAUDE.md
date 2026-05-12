# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project is

GoMarket is a **static HTML mockup website** for a prediction-market platform (think Polymarket clone). It is pure HTML/CSS/JS — no build step, no framework, no package manager. Pages are served directly as files; Vercel handles deployment (`vercel.json` is the only config file).

## Pages

| File | Purpose |
|---|---|
| `index.html` | Landing page — hero, live market cards, waitlist CTAs |
| `contact.html` | Contact form page |
| `terms.html` | Terms of service |
| `privacy.html` | Privacy policy |
| `affiliate.html` | KOL / affiliate program page |

## Development

Open any `.html` file directly in a browser, or use a local server:

```
# Python (no install needed)
python -m http.server 8080

# Node (if npx available)
npx serve .
```

No build, lint, or test commands exist — this is a hand-authored static site.

## Architecture & conventions

**Single-file pages.** Each page is fully self-contained: `<style>` block at the top, markup in `<body>`, `<script>` at the bottom. No external CSS/JS files except:
- AOS (Animate On Scroll) via CDN for scroll-in animations
- GoMarket SVG logo — inlined everywhere it appears (nav, footer, modal) using the same path data

**CSS custom properties** are declared once on `:root` in every page and shared throughout that file:
```
--purple, --mint, --navy, --sky   ← brand palette
--bg, --bg2, --bg3, --card-bg    ← dark-mode surfaces
--border                          ← rgba(137,84,242,.18)
--text, --muted                   ← typography
--grad, --grad2                   ← linear gradients
```

**Light mode** is toggled by adding `.light` to `<body>` and overriding the same CSS vars. Preference is persisted in `localStorage` under the key `gm-theme`.

**Modal system** (sign-in / wallet connect) lives in `index.html` and has three states rendered as sibling `<div>` blocks shown/hidden with `display:none`:
1. `#stateConnect` — wallet list + email waitlist fallback
2. `#stateConnecting` — spinner
3. `#stateDenied` — "wallet not on beta list" + email waitlist

All buy/trade buttons call `openModal()` — nothing actually executes a trade. The site is a visual mockup only.

**Market cards** on the landing page use a `.card-lock-overlay` that appears on hover, reinforcing the closed-beta feel. Buy Yes / Buy No buttons also trigger `openModal()`.

## Deployment

Push to `main` → Vercel auto-deploys. `vercel.json` contains routing config; check it before adding new pages to ensure clean URLs work.
