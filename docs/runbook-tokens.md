# Token Rotation Runbook -- Auto-Affi

> Last reviewed: 2026-05-13
> Owner: ops team

## Token Inventory

| Token | Env Var | Rotation Cadence | Notes |
|-------|---------|-----------------|-------|
| Meta IG long-lived page token | `AUTO_AFFI__META_ACCESS_TOKEN` | 60 days | Must re-exchange before expiry |
| Shopee Affiliate App ID + Secret | `AUTO_AFFI__SHOPEE_APP_ID`, `AUTO_AFFI__SHOPEE_SECRET` | 90 days | Regenerate via Shopee Partner Center |
| Phaya API key | `AUTO_AFFI__PHAYA_API_KEY` | 90 days | Regenerate via phaya.io dashboard |
| Anthropic API key | `AUTO_AFFI__ANTHROPIC_API_KEY` | 90 days | Regenerate via console.anthropic.com |
| ElevenLabs API key | `AUTO_AFFI__ELEVENLABS_API_KEY` | 90 days | Regenerate via elevenlabs.io |
| GCS service account JSON | `GOOGLE_APPLICATION_CREDENTIALS` | 365 days | Rotate key via gcloud IAM |
| YouTube OAuth refresh token | `AUTO_AFFI__YT_REFRESH_TOKEN` | Never expires | But revoke + re-auth if compromised |

## Meta IG Token Rotation (every 60 days)

Meta long-lived page tokens expire after 60 days. The rotation flow:

1. Get a fresh short-lived user token from Graph Explorer or OAuth flow
2. Exchange for long-lived token:
   ```
   GET /oauth/access_token?grant_type=fb_exchange_token
       &client_id={app-id}&client_secret={app-secret}
       &fb_exchange_token={short-lived-token}
   ```
3. Get page token from long-lived user token:
   ```
   GET /{user-id}/accounts?access_token={long-lived-user-token}
   ```
4. Update env var: `AUTO_AFFI__META_ACCESS_TOKEN`
5. Verify: `.venv/bin/python -c "from auto_affi.adapters.publisher import IGReelsConfig; ..."`

Set calendar reminder for day 55 (5 days before expiry).

## Shopee Affiliate Token Rotation (every 90 days)

1. Log into Shopee Partner Center
2. Navigate to App Management > API Keys
3. Regenerate secret (old one is immediately invalidated)
4. Update env vars: `AUTO_AFFI__SHOPEE_APP_ID`, `AUTO_AFFI__SHOPEE_SECRET`
5. Verify: `.venv/bin/python -c "from auto_affi.adapters.shopee import ShopeeClient; ..."`

## Phaya API Key Rotation (every 90 days)

1. Log into phaya.io dashboard
2. Account > API Keys > Generate New Key
3. Delete old key after new one is verified
4. Update env var: `AUTO_AFFI__PHAYA_API_KEY`
5. Verify: `.venv/bin/python -c "from auto_affi.adapters.phaya import PhayaClient; ..."`

## Emergency Revocation

If any token is compromised:
1. Immediately revoke via the provider's dashboard
2. Activate global kill switch: `registry.activate(KillLevel.GLOBAL, "global", reason="token compromise")`
3. Generate new token
4. Update env var
5. Deactivate kill switch after verification
6. Log incident in `.aegis/brain/logs/activity.log`

## Storage

- Dev: `.env` file (gitignored)
- Staging/Prod: Vault / SOPS (per NFR-SEC-01)
- Never commit tokens to git
