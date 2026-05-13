"""Unit tests for the GCS storage adapter — no live calls.

The google-cloud-storage SDK is fully mocked at the client/bucket/blob
layer so these tests are pure & fast.
"""

from __future__ import annotations

from datetime import timedelta
from unittest.mock import MagicMock

import pytest

from auto_affi.adapters.gcs_storage import GcsStorage, StoredAsset
from auto_affi.exceptions import AdapterError


def _mock_client(bucket_name: str) -> tuple[MagicMock, MagicMock, MagicMock]:
    """Build a mocked storage.Client → bucket → blob graph."""
    client = MagicMock(name="client")
    bucket = MagicMock(name="bucket")
    bucket.name = bucket_name
    blob = MagicMock(name="blob")
    blob.size = 42
    blob.content_type = "video/mp4"
    blob.md5_hash = "fake-md5=="
    bucket.blob.return_value = blob
    client.bucket.return_value = bucket
    return client, bucket, blob


@pytest.mark.unit
def test_rejects_missing_bucket_name(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("AUTO_AFFI__GCS_BUCKET", raising=False)
    client, _, _ = _mock_client("ignored")
    with pytest.raises(AdapterError, match="bucket name not provided"):
        GcsStorage(bucket_name=None, client=client)


@pytest.mark.unit
def test_resolves_bucket_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("AUTO_AFFI__GCS_BUCKET", "auto-affi-media-dev")
    client, bucket, _ = _mock_client("auto-affi-media-dev")
    gcs = GcsStorage(bucket_name=None, client=client)
    assert gcs.bucket_name == "auto-affi-media-dev"
    client.bucket.assert_called_once_with("auto-affi-media-dev")


@pytest.mark.unit
def test_upload_bytes_returns_gs_uri_and_metadata() -> None:
    client, bucket, blob = _mock_client("auto-affi-media-dev")
    gcs = GcsStorage(bucket_name="auto-affi-media-dev", client=client)
    result = gcs.upload_bytes(
        b"hello", key="demo/x.txt", content_type="text/plain"
    )
    bucket.blob.assert_called_once_with("demo/x.txt")
    blob.upload_from_string.assert_called_once_with(b"hello", content_type="text/plain")
    blob.reload.assert_called_once()
    assert isinstance(result, StoredAsset)
    assert result.gs_uri == "gs://auto-affi-media-dev/demo/x.txt"
    assert result.bucket == "auto-affi-media-dev"
    assert result.key == "demo/x.txt"
    assert result.size_bytes == 42
    assert result.content_type == "video/mp4"
    assert result.md5_hex == "fake-md5=="


@pytest.mark.unit
def test_upload_bytes_applies_cache_control_when_given() -> None:
    client, _bucket, blob = _mock_client("b")
    gcs = GcsStorage(bucket_name="b", client=client)
    gcs.upload_bytes(
        b"x", key="k", content_type="text/plain", cache_control="public, max-age=3600"
    )
    assert blob.cache_control == "public, max-age=3600"


@pytest.mark.unit
def test_upload_file_streams_from_path(tmp_path) -> None:
    src = tmp_path / "asset.mp4"
    src.write_bytes(b"\x00" * 100)
    client, _bucket, blob = _mock_client("b")
    gcs = GcsStorage(bucket_name="b", client=client)
    result = gcs.upload_file(src, key="vids/asset.mp4", content_type="video/mp4")
    blob.upload_from_filename.assert_called_once_with(str(src), content_type="video/mp4")
    assert result.gs_uri == "gs://b/vids/asset.mp4"


@pytest.mark.unit
def test_signed_url_uses_v4_with_ttl() -> None:
    client, _bucket, blob = _mock_client("b")
    blob.generate_signed_url.return_value = "https://signed.example/x?token=abc"
    gcs = GcsStorage(bucket_name="b", client=client)
    url = gcs.signed_url("vids/x.mp4", ttl=timedelta(minutes=15))
    blob.generate_signed_url.assert_called_once_with(
        version="v4", expiration=timedelta(minutes=15), method="GET"
    )
    assert url == "https://signed.example/x?token=abc"


@pytest.mark.unit
def test_delete_calls_blob_delete() -> None:
    client, _bucket, blob = _mock_client("b")
    gcs = GcsStorage(bucket_name="b", client=client)
    gcs.delete("k")
    blob.delete.assert_called_once()


@pytest.mark.unit
def test_download_to_file_parses_gs_uri(tmp_path) -> None:
    client, _bucket, blob = _mock_client("auto-affi-media-dev")
    gcs = GcsStorage(bucket_name="auto-affi-media-dev", client=client)
    dest = tmp_path / "downloaded" / "x.mp4"
    result = gcs.download_to_file("gs://auto-affi-media-dev/path/to/x.mp4", dest)
    assert result == dest
    _bucket.blob.assert_called_with("path/to/x.mp4")
    blob.download_to_filename.assert_called_once_with(str(dest))
    # parent dir auto-created
    assert dest.parent.exists()


@pytest.mark.unit
def test_download_rejects_non_gs_uri(tmp_path) -> None:
    client, _, _ = _mock_client("b")
    gcs = GcsStorage(bucket_name="b", client=client)
    from auto_affi.exceptions import AdapterError
    with pytest.raises(AdapterError, match="not a gs:// URI"):
        gcs.download_to_file("https://example.com/x", tmp_path / "x")
    with pytest.raises(AdapterError, match="missing object key"):
        gcs.download_to_file("gs://just-bucket", tmp_path / "x")
