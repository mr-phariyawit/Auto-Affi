"""Project-wide exception hierarchy.

Each subsystem raises a subclass of AutoAffiError so callers can match the
boundary they care about without resorting to bare Exception catches.
"""

from __future__ import annotations


class AutoAffiError(Exception):
    """Base for every Auto-Affi-raised exception."""


class ConfigError(AutoAffiError):
    """Misconfiguration detected at startup or first use."""


class AdapterError(AutoAffiError):
    """External vendor adapter failure (Shopee, kie.ai, ElevenLabs, ...)."""


class RateLimitError(AdapterError):
    """Vendor returned a rate-limit signal; backoff and retry."""


class ToolBudgetExceeded(AutoAffiError):
    """An agent exceeded its per-turn tool-call budget."""


class TokenBudgetExceeded(AutoAffiError):
    """An agent or workflow exceeded its token / cost budget."""


class SafetyViolation(AutoAffiError):
    """Output blocked by Safety / Critic agent pre-publish gate."""


class SchemaValidationError(AutoAffiError):
    """A cross-boundary handoff failed schema validation."""
