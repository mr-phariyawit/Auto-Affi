"""GCS storage adapter — owns Auto-Affi media staging per ADR-006.

Phaya and other generation vendors return assets on **their** storage
(Supabase, S3, CDN URLs). Per ADR-006, we never persist or share those
URLs downstream. Instead, we download once, push to our GCS bucket
``gs://auto-affi-media-<env>``, and reference only the resulting
``gs://`` URI in DB, Wiki, posting schedule, and analytics.

This module is the thin write path: bytes-in → ``gs://`` URI-out, with
optional signed-URL minting for time-bounded public access during the
publishing step.

Auth: Application Default Credentials via the SA JSON at
``GOOGLE_APPLICATION_CREDENTIALS``. The SA is bucket-scoped
(``roles/storage.objectAdmin`` on the bucket only — not project-wide).

Cost (May 2026, asia-southeast1):
- Standard storage: ~$0.020 / GB-month
- Class A ops (writes): $0.005 / 1k ops  → 5 videos/day = $0.00075/mo
- Egress to internet: $0.12 / GB → 5 MB/video × 5 videos/day = $0.09/mo
Both negligible at Phase 1 scale; budget impact captured in cost-model.md.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import timedelta
from pathlib import Path
from typing import Final

from google.cloud import storage
from google.cloud.storage import Bucket

from auto_affi.exceptions import AdapterError

_DEFAULT_BUCKET_ENV: Final[str] = "AUTO_AFFI__GCS_BUCKET"
_CREDS_ENV: Final[str] = "GOOGLE_APPLICATION_CREDENTIALS"


@dataclass(frozen=True, slots=True)
class StoredAsset:
    """Result of pushing a generated asset to GCS."""

    gs_uri: str
    bucket: str
    key: str
    size_bytes: int
    content_type: str
    md5_hex: str | None = None


def _resolve_bucket(client: storage.Client, bucket_name: str | None) -> Bucket:
    if not bucket_name:
        bucket_name = os.environ.get(_DEFAULT_BUCKET_ENV)
    if not bucket_name:
        raise AdapterError(
            f"GCS: bucket name not provided and {_DEFAULT_BUCKET_ENV} is not set"
        )
    return client.bucket(bucket_name)


def _build_client(credentials_path: str | None) -> storage.Client:
    if credentials_path:
        return storage.Client.from_service_account_json(credentials_path)
    env_path = os.environ.get(_CREDS_ENV)
    if env_path:
        return storage.Client.from_service_account_json(env_path)
    # Fall back to ADC (e.g. running on a GCE / Cloud Run instance with
    # workload identity); this lets us deploy to GCP without the JSON key.
    return storage.Client()


class GcsStorage:
    """Thin write/read path for the Auto-Affi media bucket.

    Construct one per process and reuse — the underlying gRPC channel pools.
    """

    def __init__(
        self,
        *,
        bucket_name: str | None = None,
        credentials_path: str | None = None,
        client: storage.Client | None = None,
    ) -> None:
        self._client = client or _build_client(credentials_path)
        self._bucket = _resolve_bucket(self._client, bucket_name)

    @property
    def bucket_name(self) -> str:
        return self._bucket.name

    def upload_bytes(
        self,
        data: bytes,
        *,
        key: str,
        content_type: str,
        cache_control: str | None = None,
    ) -> StoredAsset:
        """Upload bytes to ``gs://<bucket>/<key>``. Idempotent on key reuse."""
        blob = self._bucket.blob(key)
        if cache_control:
            blob.cache_control = cache_control
        blob.upload_from_string(data, content_type=content_type)
        blob.reload()
        return StoredAsset(
            gs_uri=f"gs://{self._bucket.name}/{key}",
            bucket=self._bucket.name,
            key=key,
            size_bytes=int(blob.size or len(data)),
            content_type=blob.content_type or content_type,
            md5_hex=blob.md5_hash,
        )

    def upload_file(
        self,
        src: Path,
        *,
        key: str,
        content_type: str,
        cache_control: str | None = None,
    ) -> StoredAsset:
        """Stream a local file to ``gs://<bucket>/<key>``."""
        blob = self._bucket.blob(key)
        if cache_control:
            blob.cache_control = cache_control
        blob.upload_from_filename(str(src), content_type=content_type)
        blob.reload()
        return StoredAsset(
            gs_uri=f"gs://{self._bucket.name}/{key}",
            bucket=self._bucket.name,
            key=key,
            size_bytes=int(blob.size or src.stat().st_size),
            content_type=blob.content_type or content_type,
            md5_hex=blob.md5_hash,
        )

    def download_to_file(self, gs_uri: str, dest: Path) -> Path:
        """Download a ``gs://<bucket>/<key>`` URI to a local file.

        Raises :class:`AdapterError` if the URI is malformed or the
        bucket doesn't match this client.
        """
        if not gs_uri.startswith("gs://"):
            raise AdapterError(f"GCS: not a gs:// URI: {gs_uri!r}")
        without_scheme = gs_uri[len("gs://"):]
        bucket_name, _, key = without_scheme.partition("/")
        if not key:
            raise AdapterError(f"GCS: missing object key in {gs_uri!r}")
        if bucket_name != self._bucket.name:
            # Allow cross-bucket reads via the same client
            blob = self._client.bucket(bucket_name).blob(key)
        else:
            blob = self._bucket.blob(key)
        dest.parent.mkdir(parents=True, exist_ok=True)
        blob.download_to_filename(str(dest))
        return dest

    def signed_url(self, key: str, *, ttl: timedelta = timedelta(hours=1)) -> str:
        """Mint a V4 signed URL for time-bounded public access (publishing step)."""
        blob = self._bucket.blob(key)
        return blob.generate_signed_url(version="v4", expiration=ttl, method="GET")

    def delete(self, key: str) -> None:
        self._bucket.blob(key).delete()
