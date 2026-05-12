"""Canonical hook-pattern library for the Writers' Room.

Six templates seeded as ``WikiTier.CANONICAL`` on Day 1, per
``docs/execution-playbook.md`` §5.1. Strategist + Screenwriter retrieve from
these before drafting; Critic validates compliance against the matching
``when_not_to_use`` clauses.

Every template includes >= 3 Thai examples written in the KOS voice (not
influencer voice) per the viral-video research note.
"""

from __future__ import annotations

from typing import Final

from pydantic import BaseModel, Field

from auto_affi.wiki.entry import WikiEntry, WikiNamespace, WikiTier


class HookTemplate(BaseModel):
    """Structured hook pattern that an agent can pick from."""

    slug: str = Field(min_length=1, pattern=r"^[a-z0-9_-]+$")
    name_th: str
    name_en: str
    description: str
    structure: list[str] = Field(min_length=1)
    thai_examples: list[str] = Field(min_length=3)
    best_for: list[str] = Field(min_length=1)
    avoid_when: list[str] = Field(min_length=1)
    max_hook_duration_s: float = Field(gt=0, le=2.0, default=1.5)


HOOK_TEMPLATES: Final[tuple[HookTemplate, ...]] = (
    HookTemplate(
        slug="pov_self_identification",
        name_th="POV ส่องตัวตน",
        name_en="POV / Self-Identification",
        description=(
            "Open with a POV frame that targets the viewer's pain or identity so "
            "they self-select in the first 1.5 seconds."
        ),
        structure=[
            "POV header on-screen (Thai)",
            "Subject inside the frame embodies the pain",
            "Implied promise of resolution after the hook",
        ],
        thai_examples=[
            "POV: คนผิวมันที่หาครีมไม่เจอสักที",
            "POV: แม่ลูกอ่อนที่นอนแค่ 3 ชั่วโมงต่อคืน",
            "POV: คนที่กดสั่งของจาก Shopee ทุกสิ้นเดือน",
        ],
        best_for=[
            "beauty_skincare",
            "mom_baby",
            "audience with a clear pain identity",
        ],
        avoid_when=[
            "Audience is broad / general consumer",
            "Product solves no identifiable pain",
        ],
    ),
    HookTemplate(
        slug="contrarian_no_one_talks",
        name_th="ของลับที่ไม่มีใครพูดถึง",
        name_en="Contrarian / No One Talks About This",
        description=(
            "Position the creator as insider authority by claiming the product "
            "is under-discussed despite working. Drives curiosity-loop completion."
        ),
        structure=[
            "Contrarian claim in voice-over",
            "Single product reveal at end of hook",
            "Tease the proof that follows",
        ],
        thai_examples=[
            "ไม่มีใครพูดถึง แต่ของชิ้นนี้เปลี่ยนชีวิตฉัน",
            "ของถูกที่ Shopee ที่คนใช้แล้วไม่บอกใคร",
            "ทุกคนซื้อแบรนด์ดัง แต่ของจริงราคาหลักร้อย",
        ],
        best_for=[
            "Lesser-known SKU with strong rating",
            "Niche audiences",
        ],
        avoid_when=[
            "Mass-market SKU already saturated on TikTok",
            "Brand legally requires standard messaging",
        ],
    ),
    HookTemplate(
        slug="numbers_scarcity",
        name_th="ตัวเลขจำกัด",
        name_en="Numbers + Scarcity",
        description=(
            "Lead with a finite count or a closing window to manufacture watch "
            "intent. Compliance: scarcity must be true; no fake countdowns."
        ),
        structure=[
            "Numerical claim in first 1 second",
            "Brief preview of each item",
            "CTA before close",
        ],
        thai_examples=[
            "3 ของจาก Shopee ที่ใช้แล้วจะไม่กลับไปใช้ของเดิม",
            "5 ไอเทมที่แม่ค้าตัวจริงแอบใช้",
            "2 สิ่งที่ขายดีตลอด 30 วันที่ผ่านมา",
        ],
        best_for=[
            "Bundle / list-style content",
            "Mega-sale lead-up videos",
        ],
        avoid_when=[
            "Stock or deadline is fabricated",
            "Product has no comparable peers to list against",
        ],
    ),
    HookTemplate(
        slug="problem_agitate_solve",
        name_th="ปัญหา-กระตุก-แก้",
        name_en="Problem-Agitate-Solve (PAS)",
        description=(
            "Surface a specific pain (1s), agitate cost-of-inaction (1s), "
            "deliver the product as solution (rest of the video)."
        ),
        structure=[
            "Pain statement in opening shot",
            "Agitate with a concrete failure mode",
            "Solution reveal at second 3",
        ],
        thai_examples=[
            "ผิวมันแบบเทเลย ใช้อะไรก็ไม่ดีขึ้น สุดท้ายเจอตัวนี้",
            "ปวดหลังจากนั่งทำงานนาน หลังเริ่มเสีย เลยลองหมอนตัวนี้",
            "ลูกแพ้ผงซักฟอกทั่วไปจนผื่นขึ้น เปลี่ยนมาใช้สูตรนี้",
        ],
        best_for=[
            "Functional products with a clear pain narrative",
            "Beauty, baby, home utility",
        ],
        avoid_when=[
            "Pain is medical / requires diagnosis (compliance hard-block)",
            "Product cannot demonstrate the solve on camera",
        ],
    ),
    HookTemplate(
        slug="before_after_demo",
        name_th="ก่อน-หลัง",
        name_en="Before / After Demo",
        description=(
            "Show visual delta inside the first 3 seconds — highest "
            "save-rate hook in the viral-video research."
        ),
        structure=[
            "Before state on-screen (real, unfiltered)",
            "Match-cut to after state",
            "Product label visible at transition",
        ],
        thai_examples=[
            "ผมหยิก 30 วินาทีหลังใช้ น่าจะเห็นชัด",
            "ห้องรกแค่ไหน หลังใช้ตัวนี้ใน 1 นาที",
            "หน้ามัน 9 โมงเช้า กับ 6 โมงเย็นหลังลงไพรเมอร์ตัวนี้",
        ],
        best_for=[
            "Visual delta is real and repeatable",
            "Beauty, home, organisation, food prep",
        ],
        avoid_when=[
            "Visual change requires editing tricks",
            "Compliance: any health/whitening claim must be removed",
        ],
    ),
    HookTemplate(
        slug="open_loop",
        name_th="เปิดวงจรค้างไว้",
        name_en="Open Loop",
        description=(
            "Tell the viewer not to leave — explicit retention prompt that "
            "lifts completion rate above the 70% viral threshold."
        ),
        structure=[
            "Explicit 'wait until the end' line",
            "Tease the payoff without revealing",
            "Deliver payoff in the final scene",
        ],
        thai_examples=[
            "อย่าเพิ่งปิด รอดูตอนจบ",
            "ตอนท้ายจะมีของแถมที่หาไม่ได้ที่อื่น",
            "อันสุดท้ายคืออันที่ทุกคนยังไม่เคยเห็น",
        ],
        best_for=[
            "List videos with a hero item at the end",
            "Drops where the punchline lives in the last 2 seconds",
        ],
        avoid_when=[
            "Payoff is not actually unique",
            "Video has no scripted climax",
        ],
    ),
)


def all_templates() -> tuple[HookTemplate, ...]:
    """Return the canonical hook template tuple."""
    return HOOK_TEMPLATES


def by_slug(slug: str) -> HookTemplate:
    """Look up a template by slug, raising :class:`KeyError` if missing."""
    for template in HOOK_TEMPLATES:
        if template.slug == slug:
            return template
    raise KeyError(slug)


def to_wiki_entries() -> list[WikiEntry]:
    """Materialise the library as canonical wiki entries ready for seeding."""
    entries: list[WikiEntry] = []
    for template in HOOK_TEMPLATES:
        entries.append(
            WikiEntry(
                slug=f"hook-{template.slug}",
                namespace=WikiNamespace.HOOK_PATTERN,
                tier=WikiTier.CANONICAL,
                title=f"{template.name_th} ({template.name_en})",
                summary=template.description,
                payload=template.model_dump(),
                tags=["hook", "thai", "canonical-day1", *template.best_for],
            )
        )
    return entries
