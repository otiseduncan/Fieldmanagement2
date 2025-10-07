# Deployment Guide

This guide outlines the deployment process for FieldService 2 to Google Cloud Run. Adjust the steps to fit your CI/CD tooling and target environments.

## Prerequisites

- Google Cloud project with billing enabled.
- Service account with permissions for Cloud Run, Cloud SQL, Artifact Registry, and Cloud Storage.
- Cloud SQL PostgreSQL instance provisioned (or plan to create during deployment).
- Artifact Registry repository for container images.
- Google Cloud SDK installed locally or in CI runners.

## 1. Provision Infrastructure

1. Create a Cloud SQL PostgreSQL instance and note the connection string.
2. Create a Cloud Storage bucket for technician uploads.
3. (Optional) Enable Firestore in Native Mode for audit logging.
4. Grant the FieldService service account access to the bucket and database.

## 2. Build Container Images

```bash
# Backend
 gcloud builds submit --tag us-central1-docker.pkg.dev/$PROJECT_ID/fieldservice2/backend ./backend

# Frontend
 gcloud builds submit --tag us-central1-docker.pkg.dev/$PROJECT_ID/fieldservice2/frontend ./frontend
```

## 3. Deploy to Cloud Run

```bash
gcloud run deploy fieldservice2-backend \
  --image=us-central1-docker.pkg.dev/$PROJECT_ID/fieldservice2/backend \
  --region=$REGION \
  --allow-unauthenticated \
  --set-env-vars=DATABASE_URL=$DATABASE_URL,SECRET_KEY=$SECRET_KEY,GCS_BUCKET=$BUCKET,GOOGLE_PROJECT_ID=$PROJECT_ID

gcloud run deploy fieldservice2-frontend \
  --image=us-central1-docker.pkg.dev/$PROJECT_ID/fieldservice2/frontend \
  --region=$REGION \
  --allow-unauthenticated \
  --set-env-vars=VITE_API_URL=$BACKEND_URL
```

## 4. Configure Secrets

Store sensitive configuration (JWT secrets, database credentials, service-account JSON) in Secret Manager and mount them into Cloud Run via environment variables or volumes.

## 5. Database Migrations

Run Alembic migrations against Cloud SQL using the service account:

```bash
alembic upgrade head
```

Configure a Cloud Build trigger or GitHub Action workflow that runs migrations after each deployment.

## 6. Observability

- Enable Cloud Logging and Cloud Monitoring dashboards.
- Send FastAPI logs in JSON format (already configured) for Stackdriver ingestion.
- Configure alerts for error rates, latency, and CPU utilization.

## 7. Post-Deployment Checklist

- Verify `/health` endpoint responds with `200`.
- Ensure technicians can authenticate and fetch job lists.
- Upload sample images to validate Cloud Storage permissions.
- Confirm client job submissions reach the database.

For further automation guidance see future updates in `.github/workflows/` (to be added).
