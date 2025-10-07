# FieldService 2

FieldService 2 is a cloud-native platform for managing ADAS calibration jobs across technicians, client service managers, and enterprise administrators. This documentation hub complements the project-level README and covers architecture decisions, API behaviors, deployment runbooks, and roadmap planning.

- [API Specification](./API_SPEC.md)
- [Deployment Guide](./DEPLOYMENT.md)
- [Product Roadmap](./ROADMAP.md)

## Local Development

1. Create a `.env` file based on `.env.example` and provide Google Cloud credentials under `./secrets/service_account.json`.
2. Launch services with `docker compose up --build`.
3. Access the backend at http://localhost:8000/docs and the frontend at http://localhost:5173.

## High-Level Architecture

- **Frontend**: React + Vite single page application with Tailwind CSS and Zustand for state composition.
- **Backend**: FastAPI with SQLAlchemy, PostgreSQL, and Google Cloud integrations for storage and Firestore logging.
- **Infrastructure**: Docker Compose for local orchestration, Alembic for schema migrations, and GitHub Actions (planned) for CI/CD.

For deeper design context see [ROADMAP.md](./ROADMAP.md) and the inline ADR comments within the source tree.
