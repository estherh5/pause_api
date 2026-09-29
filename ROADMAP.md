# Roadmap

Committed doc, not scratch. Kept current by hand as work ships.
**Shipped** = live in production. **Next** = intended, not promised.
**Declined** = decided against, with the reason, so it doesn't get re-proposed.
**Open questions** = unresolved calls, with what would settle them.

## Shipped

- **2026-09** **Anonymous POST is bounded; CORS is pause-only.** `server.py#create_app` caps
  request bodies at 64 KB (413) and defaults `CORS_ORIGINS` to `https://pause.crystalprism.io`
  instead of `*`. `pause/pause.py#create_activities` refuses with 429 once `CREATE_LIMIT` (10)
  rows were created in the last `CREATE_WINDOW` (1 hour). The limit is global and counted from
  the DB, so it holds across serverless instances and stores nothing about who posted. Prod had 4
  rows ever (largest 678 bytes), so real use never gets near either cap.

- **2026-09** **Pushes to `main` deploy.** The Vercel project is now git-connected (production
  branch `main`); before this, only `vercel --prod` deployed it, and a push produced no build.

- **2026-09** **Heroku decommissioned.** The `pause-app-api` app and its add-ons were destroyed on
  2026-09-04 after three days of parallel running with zero real traffic. A final pre-destroy dump
  was taken and row-matched against Neon on every table before deletion. Its scheduler add-on held no active job.

- **2026-09** **Off Heroku onto Vercel.** The API is served from `pause-api.crystalprism.io`;
  `pause`'s `src/App.jsx` points its `PRODUCTION_API_URL` there. It keeps using the
  `crystalprism` database, now on Neon (project `old-sun-58330819`, PostgreSQL 18), shared with
  the main API and vroom, so it is covered by that database's nightly dump.

## Next

## Declined

- **CORS headers on `/health`** (decided 2026-09). Only `/api/*` gets CORS in `server.py`'s
  `create_app`. `/health` is for machines (curl, uptime checks). No page reads it, and its
  constant `{"status": "ok"}` is not worth reading from a page. If a page ever needs it, that
  missing header is why the request fails: add `r"/health"` to the `resources` passed to `CORS`
  in `create_app`, a one-line change.
