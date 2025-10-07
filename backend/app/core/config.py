from functools import lru_cache
from typing import List

from pydantic import AnyHttpUrl, Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    project_name: str = Field('FieldService 2 API', alias='PROJECT_NAME')
    environment: str = Field('local', alias='ENVIRONMENT')
    api_v1_prefix: str = Field('/api/v1', alias='API_V1_PREFIX')

    secret_key: str = Field('change-me', alias='SECRET_KEY')
    algorithm: str = Field('HS256', alias='ALGORITHM')
    access_token_expire_minutes: int = Field(60, alias='ACCESS_TOKEN_EXPIRE_MINUTES')

    database_url: str = Field(
        'postgresql+psycopg2://postgres:postgres@db:5432/fieldservice2',
        alias='DATABASE_URL',
    )

    cors_origins: List[AnyHttpUrl | str] = Field(
        default_factory=lambda: ['http://localhost:5173'],
        alias='CORS_ORIGINS',
    )

    google_project_id: str = Field('local-project', alias='GOOGLE_PROJECT_ID')
    google_application_credentials: str = Field(
        '/app/secrets/service_account.json',
        alias='GOOGLE_APPLICATION_CREDENTIALS',
    )
    gcs_bucket: str = Field('fieldservice2-uploads', alias='GCS_BUCKET')
    gcp_region: str = Field('us-central1', alias='GCP_REGION')

    sentry_dsn: str | None = Field(None, alias='SENTRY_DSN')

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        case_sensitive = False


@lru_cache
def get_settings() -> 'Settings':
    return Settings()  # type: ignore[call-arg]


settings = get_settings()
