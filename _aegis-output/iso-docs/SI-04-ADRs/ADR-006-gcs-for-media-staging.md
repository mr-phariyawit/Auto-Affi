# ADR-006 — GCS for media staging (never Phaya's supabase URLs)

- **Status**: Accepted
- **Date**: 2026-05-13
- **Decided by**: board (mr.phariyawit@gmail.com), via direct directive
- **Replaces**: implicit "trust Phaya staging URLs" pattern surfaced during demo run

## Context

Phaya.io delivers generated assets (Sora 2 video, Thai TTS audio, music,
images) via Supabase storage URLs of the form:

```
https://bvlkdbigeaecqdmkzrvc.supabase.co/storage/v1/object/public/
    media-outputs/outputs/<capability>/<user_id>/<job_id>.<ext>
```

These URLs:

- Are publicly accessible to anyone who knows the path
- Sit on Phaya's Supabase bucket, not ours
- Have no published retention SLA
- Bind our content lifecycle to a third-party vendor's bucket policy
- Mix our private generation outputs with Phaya's multi-tenant storage

## Decision

**Auto-Affi media pipeline never persists or references Phaya Supabase URLs
in any downstream system** (database, Wiki entries, posting scheduler,
analytics, publisher payloads). Instead:

1. Phaya generates → polls status → returns a Supabase result URL.
2. Adapter (or the Producer node) **immediately downloads** the bytes.
3. Bytes are **uploaded to our own GCS bucket** (`gs://auto-affi-media-<env>/`).
4. All downstream systems reference the GCS URI (or a signed CDN URL for
   public-facing posts).
5. The Supabase URL is held only as a transient handle for the download
   step; it is never logged, persisted, or shared.

## Consequences

**Positive**:
- We own the storage layer end-to-end (retention, ACL, audit, lifecycle).
- We can apply our own CDN + signed-URL policy for publishing.
- Asset survives if Phaya rotates / expires Supabase URLs.
- Privacy: no public Supabase URLs in our DB or logs.
- Cost control: GCS class A/B operations are predictable; Supabase free
  tier rate-limits could throttle high-volume publishing.

**Negative**:
- Extra network hop per asset (Phaya download + GCS upload). At Phase 1
  scale (5 videos/day × ~5 MB) the cost is trivial — ~0.025 GB/day egress
  on Phaya side, ~0.025 GB/day ingress on GCS (free).
- Adds a hard dependency on a GCP project + service-account credentials.
- Latency: adds ~1-3 s per asset depending on Phaya egress region.

## Implementation outline

1. **GCS bucket**: `gs://auto-affi-media-dev` (later `-staging`, `-prod`).
   Lifecycle: 90-day transition to Coldline; 365-day delete on non-published.
2. **Service account**: `auto-affi-media@<project>.iam.gserviceaccount.com`
   with `roles/storage.objectAdmin` on the bucket only.
3. **Credentials path**: `GOOGLE_APPLICATION_CREDENTIALS=/path/to/sa.json`
   in `.env`; never committed.
4. **New module**: `src/auto_affi/adapters/gcs_storage.py` exposing
   `upload_bytes(blob: bytes, *, key: str, content_type: str) -> str` returning
   a `gs://...` URI.
5. **Phaya adapter integration**: the `_get_status` result URL is *internal*;
   the protocol adapter (`PhayaVideoGenAdapter`, `PhayaTTSAdapter`) downloads
   then uploads, and returns a `GeneratedAsset` / `TTSResult` whose path is
   the GCS URI, not the Supabase URL.

## Out of scope for this ADR

- Choice of CDN in front of GCS (Cloud CDN vs Cloudflare). Defer to Sprint 5.
- Signed-URL policy (TTL, IAM bindings). Defer.
- Cross-region replication. Phase 2.

## Related

- [[non-goals]] — confirms no multi-region Phase 1
- [[cost-model]] — GCS cost lines must be added to per-video budget
- ADR-003 (Bilateral wiki sync) — same principle of "we own the durable store"
