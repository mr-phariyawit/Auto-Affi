"""Unit tests for the canonical hook-pattern library."""

from __future__ import annotations

import pytest

from auto_affi.wiki.entry import WikiNamespace, WikiTier
from auto_affi.wiki.hook_library import (
    HOOK_TEMPLATES,
    HookTemplate,
    all_templates,
    by_slug,
    to_wiki_entries,
)

_EXPECTED_SLUGS = frozenset(
    {
        "pov_self_identification",
        "contrarian_no_one_talks",
        "numbers_scarcity",
        "problem_agitate_solve",
        "before_after_demo",
        "open_loop",
    }
)


@pytest.mark.unit
def test_canonical_six_templates_present() -> None:
    slugs = {template.slug for template in HOOK_TEMPLATES}
    assert slugs == _EXPECTED_SLUGS


@pytest.mark.unit
@pytest.mark.parametrize("template", HOOK_TEMPLATES, ids=lambda t: t.slug)
def test_each_template_has_three_thai_examples(template: HookTemplate) -> None:
    assert len(template.thai_examples) >= 3
    for example in template.thai_examples:
        assert _contains_thai(example), example


@pytest.mark.unit
@pytest.mark.parametrize("template", HOOK_TEMPLATES, ids=lambda t: t.slug)
def test_hook_duration_within_two_seconds(template: HookTemplate) -> None:
    assert 0 < template.max_hook_duration_s <= 2.0


@pytest.mark.unit
@pytest.mark.parametrize("template", HOOK_TEMPLATES, ids=lambda t: t.slug)
def test_each_template_has_avoid_when_clause(template: HookTemplate) -> None:
    # Critic uses this list to red-team the storyboard before publish.
    assert template.avoid_when
    assert template.best_for


@pytest.mark.unit
def test_by_slug_lookup() -> None:
    assert by_slug("open_loop").name_en == "Open Loop"
    with pytest.raises(KeyError):
        by_slug("missing_template")


@pytest.mark.unit
def test_to_wiki_entries_seeds_canonical_namespace() -> None:
    entries = to_wiki_entries()
    assert len(entries) == len(HOOK_TEMPLATES)
    for entry in entries:
        assert entry.namespace is WikiNamespace.HOOK_PATTERN
        assert entry.tier is WikiTier.CANONICAL
        assert entry.slug.startswith("hook-")
        assert "hook" in entry.tags
        assert "thai" in entry.tags


@pytest.mark.unit
def test_all_templates_returns_canonical_tuple() -> None:
    assert all_templates() is HOOK_TEMPLATES


def _contains_thai(text: str) -> bool:
    return any("฀" <= ch <= "๿" for ch in text)
