"""Strategist agent — deterministic, offline-only (Phase 1).

Takes a :class:`ShopeeProduct` (from Scout) and produces a
:class:`CampaignBrief` (for Writers' Room). Fulfils FR-ST-01..03:

  - Generates a structured CampaignBrief with all required fields
  - Derives persona/angle/hook_template_slug/cta/hypothesis/expected_ctr
    from product facts + a small rule table — NO LLM, NO network
  - Boosts priority when within 14 days of a Shopee mega-sale (FR-ST-03)

Implementation: pure, deterministic template selection — zero Anthropic,
zero httpx, zero async.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from auto_affi.adapters.shopee import ShopeeProduct
from auto_affi.schemas.campaign_brief import CTA, CampaignBrief, Persona

# ---------------------------------------------------------------------------
# Mega-sale calendar (FR-ST-03)
# ---------------------------------------------------------------------------

_MEGA_SALES: tuple[tuple[int, int], ...] = (
    (1, 1),
    (2, 2),
    (2, 14),
    (3, 3),
    (4, 4),
    (4, 13),
    (5, 5),
    (6, 6),
    (7, 7),
    (8, 8),
    (8, 12),
    (9, 9),
    (10, 10),
    (11, 11),
    (12, 12),
    (12, 25),
)
_MEGA_SALE_WINDOW_DAYS = 14


def is_mega_sale_window(*, today: date | None = None) -> bool:
    """Return True if *today* is within 14 days before any Shopee mega-sale."""
    d = today or date.today()
    for month, day in _MEGA_SALES:
        try:
            sale_date = d.replace(month=month, day=day)
        except ValueError:
            continue
        delta = (sale_date - d).days
        if 0 <= delta <= _MEGA_SALE_WINDOW_DAYS:
            return True
    return False


# ---------------------------------------------------------------------------
# Template table — keyed by product signal bucket
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class _HookTemplate:
    slug: str                   # must match ^[a-z0-9_-]+$
    angle_th: str
    hook_prefix_th: str         # first 2s punch
    cta_th: str
    hypothesis_th: str
    expected_ctr: float         # must be <= 0.15


# The template table covers 5 signal buckets derived from name keywords +
# commission/price tier.  Rules evaluated top-to-bottom; first match wins.
_TEMPLATES: list[_HookTemplate] = [
    _HookTemplate(
        slug="rainy-season-must-have",
        angle_th="ฤดูฝนมาแล้ว ต้องมีติดบ้าน!",
        hook_prefix_th="ฝนมาแล้ว… คุณพร้อมแล้วหรือยัง?",
        cta_th="กดสั่งเลย ลิงก์ในไบโอ",
        hypothesis_th=(
            "สินค้ากันฝน/UV ขายดีช่วงมรสุม ราคาเข้าถึงง่าย "
            "กลุ่มเป้าหมายเห็นภาพใช้งานจริง CTR สูงกว่าค่าเฉลี่ย"
        ),
        expected_ctr=0.055,
    ),
    _HookTemplate(
        slug="price-comparison-winner",
        angle_th="ราคานี้ดีที่สุดในช็อปปี้ตอนนี้!",
        hook_prefix_th="ก่อนกด Add to Cart ดูราคานี้ก่อน!",
        cta_th="แคปภาพก่อน แล้วกดลิงก์ด้านล่าง",
        hypothesis_th=(
            "การเปรียบราคาดึงดูดนักช้อปที่ตัดสินใจยาก "
            "ราคาต่ำกว่าคู่แข่งชัดเจน กระตุ้น FOMO ได้ดี"
        ),
        expected_ctr=0.048,
    ),
    _HookTemplate(
        slug="social-proof-bestseller",
        angle_th="ยอดขายพุ่ง! ทำไมคนถึงซื้อเยอะขนาดนี้?",
        hook_prefix_th="คนซื้อไปแล้วหลายพันชิ้น คุณยังไม่มีเหรอ?",
        cta_th="ดูรีวิวจริงได้เลย กดที่ลิงก์",
        hypothesis_th=(
            "Social proof จากยอดขายสูงลดความลังเล "
            "รีวิวดาวสูงเพิ่มความเชื่อมั่น CTR ดีจากกลุ่มที่ยังลังเล"
        ),
        expected_ctr=0.062,
    ),
    _HookTemplate(
        slug="beauty-result-reveal",
        angle_th="เปิดผลลัพธ์จริง ผิวเปลี่ยนชัด!",
        hook_prefix_th="ก่อน vs หลังใช้ 7 วัน ดูนี่เลย",
        cta_th="ลองเลย ลิงก์ด้านล่าง ส่งฟรีวันนี้",
        hypothesis_th=(
            "Before/after hook ดึง attention ในเฟีดได้เร็ว "
            "กลุ่มสกินแคร์ตอบสนองต่อ result reveal สูง "
            "CTR จาก female 18-35 อยู่ในแนวดี"
        ),
        expected_ctr=0.071,
    ),
    _HookTemplate(
        slug="everyday-hero-gadget",
        angle_th="แก็ดเจ็ตชิ้นเดียว แก้ปัญหาได้ทุกวัน",
        hook_prefix_th="ปัญหานี้แก้ได้แค่ชิ้นเดียว!",
        cta_th="กดสั่งผ่านลิงก์ด้านล่าง จัดส่งด่วน",
        hypothesis_th=(
            "แก็ดเจ็ตอเนกประสงค์ดึง pain point ผู้ใช้งานประจำวัน "
            "ราคาย่อมเยา ตัดสินใจเร็ว CTR อยู่ในระดับดี"
        ),
        expected_ctr=0.043,
    ),
]

# Fallback template used when no keyword rule matches
_FALLBACK = _TEMPLATES[2]  # social-proof-bestseller


# ---------------------------------------------------------------------------
# Keyword signal detection
# ---------------------------------------------------------------------------

_RAIN_KEYWORDS = ("ร่ม", "กันฝน", "rain", "umbrella")
_BEAUTY_KEYWORDS = ("ครีม", "serum", "เซรั่ม", "SPF", "sunscreen", "กันแดด", "มาส์ก", "สกิน", "ผิว", "หน้า")
_GADGET_KEYWORDS = ("ซอง", "กระเป๋า", "พก", "สาย", "อุปกรณ์", "gadget", "pouch", "bag", "2-in-1", "กันน้ำ", "UV")


def _name_bucket(name: str) -> str | None:
    """Classify a product name into a keyword bucket (rain/beauty/gadget) or None.

    Order matters and is shared by :func:`_detect_bucket` and :func:`_build_persona`.
    """
    if any(kw in name for kw in _RAIN_KEYWORDS):
        return "rain"
    if any(kw in name for kw in _BEAUTY_KEYWORDS):
        return "beauty"
    if any(kw in name for kw in _GADGET_KEYWORDS):
        return "gadget"
    return None


def _detect_bucket(product: ShopeeProduct) -> _HookTemplate:
    """Pick the hook template that best fits the product name + price signals."""
    bucket = _name_bucket(product.name)

    if bucket == "rain":
        return _TEMPLATES[0]  # rainy-season-must-have
    if bucket == "beauty":
        return _TEMPLATES[3]  # beauty-result-reveal
    if bucket == "gadget":
        return _TEMPLATES[4]  # everyday-hero-gadget

    # High sales volume → social proof
    if product.sales >= 2000:
        return _TEMPLATES[2]  # social-proof-bestseller

    # Price comparison if cheap (<= 200 THB avg)
    avg_price = (product.price_min + product.price_max) / 2.0
    if avg_price <= 200.0:
        return _TEMPLATES[1]  # price-comparison-winner

    return _FALLBACK


# ---------------------------------------------------------------------------
# Persona derivation
# ---------------------------------------------------------------------------

def _build_persona(product: ShopeeProduct, template: _HookTemplate) -> Persona:
    """Derive a deterministic Persona from the product + template bucket."""
    bucket = _name_bucket(product.name)

    if bucket == "rain":
        return Persona(
            label="สาวออฟฟิศไทยที่เดินทางด้วยระบบขนส่งสาธารณะ",
            age_range="22-35",
            pain_points=[
                "เปียกฝนทุกวันทำงาน",
                "ร่มพับได้หนักและเทอะทะ",
                "ผิวไหม้จากแดดตอนรอรถ",
            ],
            daily_context="เดินทางด้วย BTS/MRT ทุกวัน อยู่กลางแดดกลางฝน",
        )

    if bucket == "beauty":
        return Persona(
            label="สาวไทยรักผิวที่ใส่ใจสกินแคร์",
            age_range="18-35",
            pain_points=[
                "ผิวหมองคล้ำจากแดด",
                "หาครีมกันแดดที่ไม่เยิ้มได้ยาก",
                "กลัวซื้อแล้วใช้ไม่เหมาะกับผิว",
            ],
            daily_context="ดูสกินแคร์รีวิวใน IG Reels และ TikTok ทุกวัน",
        )

    if bucket == "gadget":
        return Persona(
            label="คนทำงานที่ใช้สมาร์ตโฟนเป็นหลักทุกวัน",
            age_range="20-38",
            pain_points=[
                "โทรศัพท์เสียหายจากน้ำ",
                "กระเป๋าสะพายใบใหญ่เทอะทะเกินไป",
                "ของหายง่ายตอนออกกำลังกาย",
            ],
            daily_context="ออกกำลังกายและใช้แอปโทรศัพท์ทั้งวัน",
        )

    # Default persona
    return Persona(
        label="ผู้ซื้อออนไลน์ที่มองหาของดีราคาคุ้ม",
        age_range="20-40",
        pain_points=[
            "ไม่แน่ใจว่าสินค้าออนไลน์คุณภาพดีจริงหรือเปล่า",
            "อยากได้ของที่คุ้มค่าคุ้มราคา",
        ],
        daily_context="ช้อปออนไลน์ใน Shopee และดูรีวิวใน YouTube และ IG",
    )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def build_brief(
    product: ShopeeProduct,
    *,
    scout_score: float | None = None,
    today: date | None = None,
) -> CampaignBrief:
    """Build a deterministic CampaignBrief from a ShopeeProduct.

    Parameters
    ----------
    product:
        The Shopee product candidate from the Scout agent.
    scout_score:
        Optional numeric score (0-1) from the Scout rubric. When provided
        and high (>= 0.6) it slightly adjusts expected_ctr upward.
    today:
        Override today's date (for testability of the mega-sale window check).

    Returns
    -------
    CampaignBrief
        A fully-populated, schema-validated brief ready for the Writers' Room.
    """
    template = _detect_bucket(product)
    persona = _build_persona(product, template)
    boost = is_mega_sale_window(today=today)

    # Adjust CTR slightly when scout score is high
    ctr = template.expected_ctr
    if scout_score is not None and scout_score >= 0.6:
        ctr = min(ctr * 1.15, 0.14)  # bump up to 15% floor minus headroom

    avg_price = (product.price_min + product.price_max) / 2.0

    angle = (
        f"{template.angle_th} — {product.name[:60]} ราคาเฉลี่ย {avg_price:.0f} บาท"
        f" คอมมิชชั่น {product.commission_rate * 100:.0f}%"
    )

    hypothesis = (
        f"{template.hypothesis_th} "
        f"สินค้า: {product.name[:40]} ราคา {avg_price:.0f} THB "
        f"ดาว {product.rating_star}/5 ยอดขาย {product.sales} ชิ้น"
    )

    return CampaignBrief(
        product_id=product.item_id,
        shop_id=product.shop_id,
        persona=persona,
        angle=angle[:200],
        hook_template_slug=template.slug,
        cta=CTA(
            text_th=template.cta_th,
            placement="end-card",
        ),
        hypothesis=hypothesis[:300],
        expected_ctr=round(ctr, 4),
        confidence=round(
            min(
                0.5
                + (min(product.sales, 5000) / 10000.0)
                + (product.rating_star - 4.0) / 4.0,
                1.0,
            ),
            3,
        ),
        priority_boost=boost,
        wiki_evidence_slugs=[template.slug],
    )
