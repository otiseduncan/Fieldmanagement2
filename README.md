# FieldService 2

FieldService 2 is a multi-tenant platform for orchestrating ADAS calibration workflows across technicians, client service managers, administrators, and customer portals. This repository contains:

- **backend/** — FastAPI service with PostgreSQL, JWT auth, and Google Cloud integrations.
- **frontend/** — React + Vite SPA with Tailwind CSS and state providers.
- **database/** — SQL bootstrapping scripts for local development.
- **docs/** — Architecture overview, API spec, deployment guide, and roadmap.

## Getting Started

1. Duplicate `.env.example` to `.env` and adjust secrets.
2. Place your Google service account JSON at `./secrets/service_account.json`.
3. Run `docker compose up --build` to start Postgres, FastAPI, and Vite dev server.
4. Visit http://localhost:5173 for the frontend and http://localhost:8000/docs for API docs.

## Tech Stack

- Python 3.12, FastAPI, SQLAlchemy, Alembic
- PostgreSQL 16, Docker Compose
- React 18, Vite, Tailwind CSS, Axios, Zustand
- Google Cloud Storage & Firestore clients scaffolded for asset storage and logging

## Development Notes

- Default seeded credentials: `admin@example.com` / `admin123` (for local only).
- Backend includes starter tests under `backend/tests/` (run with `pytest`).
- Frontend lints via `npm run lint` and builds with `npm run build`.

See [`docs/`](./docs/README.md) for detailed planning and deployment documentation.
