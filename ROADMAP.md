# Roadmap

Committed doc, not scratch. Kept current by hand as work ships.
**Shipped** = live in production. **Next** = intended, not promised.
**Declined** = decided against, with the reason, so it doesn't get re-proposed.
**Open questions** = unresolved calls, with what would settle them.

## Shipped

- **2026-09** **Off Heroku onto Vercel.** The API is served from `pause-api.crystalprism.io`;
  `pause`'s `src/App.jsx` points its `PRODUCTION_API_URL` there. It keeps using the
  `crystalprism` database, now on Neon (project `old-sun-58330819`, PostgreSQL 18), shared with
  the main API and vroom, so it is covered by that database's nightly dump.

## Open questions

- `/health` has no CORS headers, unlike `/api/*`. Harmless today — the app only ever calls
  `/api/*` from a browser, and `/health` is hit by curl and uptime checks — but if anything ever
  needs to read it from a page, that is the reason it will fail.
