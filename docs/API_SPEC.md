# API Specification

Version: 0.1.0
Base URL: `/api/v1`

## Authentication

- **POST** `/auth/login`
  - Request: `application/x-www-form-urlencoded` with `username`, `password`.
  - Response: `200 OK` `{ "access_token": string, "token_type": "bearer" }`
  - Errors: `401 Unauthorized` when credentials invalid.

## Users

- **GET** `/users/me`
  - Returns the authenticated user profile.
  - Requires: `Authorization: Bearer <token>`

## Jobs

- **GET** `/jobs`
  - Returns paginated list of jobs (prototype implementation returns all records).

- **POST** `/jobs`
  - Creates a new job and returns the persisted entity.
  - Body: `JobCreate`

- **GET** `/jobs/{job_id}`
  - Returns a single job by identifier.

- **PATCH** `/jobs/{job_id}`
  - Partially updates a job record.

- **DELETE** `/jobs/{job_id}`
  - Soft-deletes a job (prototype performs hard delete).

## Clients

- **GET** `/clients`
- **POST** `/clients`
- **GET** `/clients/{client_id}`
- **PATCH** `/clients/{client_id}`
- **DELETE** `/clients/{client_id}`

## Reports

- **GET** `/reports/{job_id}/export`
  - Returns a plaintext report for download.

## Data Models

### User
- `id`: integer
- `email`: string
- `full_name`: string
- `roles`: array[string]
- `is_active`: boolean

### Job
- `id`: integer
- `ro_number`: string
- `vin`: string
- `status`: string
- `technician_notes`: string
- `client_notes`: string
- `metadata`: object
- `technician_id`: integer
- `client_id`: integer
- `scheduled_start`: datetime
- `scheduled_end`: datetime
- `completed_at`: datetime
- `created_at`: datetime
- `updated_at`: datetime

### Client
- `id`: integer
- `name`: string
- `primary_contact`: string
- `email`: string
- `phone`: string
- `address`: string
- `metadata`: object

> **Note**: Swagger UI is automatically available at `/docs` when the backend is running.
