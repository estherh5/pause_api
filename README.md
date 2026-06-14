# Pause API

Flask API for storing and retrieving schedules created by
[Pause](https://pause.crystalprism.io/).

## Development

The project targets Python 3.13.

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
```

For local development, the API uses `pause.db`, a SQLite database:

```sh
flask --app server run --debug
```

Set `DB_CONNECTION` or `DATABASE_URL` to use PostgreSQL instead:

```sh
export DB_CONNECTION=postgresql+psycopg2://pause_admin:password@localhost/pause
alembic upgrade head
flask --app server run --debug
```

Copy `.env.example` as a starting point for the supported environment
variables. `CORS_ORIGINS` defaults to `*`; production deployments should set it
to the Pause frontend origin.

## Checks

```sh
pytest
ruff check .
ruff format --check .
```

The test suite uses a temporary SQLite database and does not require a running
PostgreSQL server.

## API

### `POST /api/pause/activities`

Stores a schedule and returns a JSON string containing its 16-character public
identifier.

```json
{
  "activities": {
    "0": [
      {"id": 0, "label": "", "value": 16, "color": "#DCDCDC"},
      {"id": 1, "label": "sleep", "value": 8, "color": "#ff6300"}
    ]
  },
  "chartTypes": {"0": "pie"},
  "timeUnit": "day",
  "month": null,
  "year": null
}
```

### `GET /api/pause/activities/<activities_id>`

Returns the saved schedule:

```json
{
  "activities": {
    "0": [
      {"id": 0, "label": "", "value": 16, "color": "#DCDCDC"},
      {"id": 1, "label": "sleep", "value": 8, "color": "#ff6300"}
    ]
  },
  "chart_types": {"0": "pie"},
  "time_unit": "day",
  "month": null,
  "year": null
}
```

### `GET /health`

Returns `{"status": "ok"}` for platform health checks.

## Database Backups

Create and upload a PostgreSQL custom-format dump:

```sh
python management.py backup_db
```

The command requires `DB_CONNECTION`, `BACKUP_DIR`, `S3_BUCKET`, and standard
AWS credentials. `S3_BACKUP_DIR` is optional.

Schedule the command for Sundays at midnight using the current Python
interpreter:

```sh
python management.py sched_backup
```
