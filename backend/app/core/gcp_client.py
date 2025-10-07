from __future__ import annotations

import os
from functools import lru_cache
from typing import BinaryIO

from google.cloud import firestore, storage
from google.oauth2 import service_account

from app.core.config import settings


@lru_cache
def _get_credentials() -> service_account.Credentials:
    credentials_path = settings.google_application_credentials
    if not os.path.exists(credentials_path):
        raise FileNotFoundError(
            f'Google credentials not found at {credentials_path}. Place your service_account.json file there.'
        )
    return service_account.Credentials.from_service_account_file(credentials_path)


def get_storage_client() -> storage.Client:
    return storage.Client(credentials=_get_credentials(), project=settings.google_project_id)


def get_firestore_client() -> firestore.Client:
    return firestore.Client(credentials=_get_credentials(), project=settings.google_project_id)


def upload_stream_to_bucket(*, bucket_name: str, stream: BinaryIO, destination: str, content_type: str) -> str:
    """Upload a binary stream to Cloud Storage and return the gs:// path."""
    client = get_storage_client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination)
    blob.upload_from_file(stream, content_type=content_type)
    return f'gs://{bucket_name}/{destination}'
