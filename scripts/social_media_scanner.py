#!/usr/bin/env python3
"""Auto-Affi social/search/social-video trend scanner.

The scanner intentionally uses allowed/public or official-API sources first.
It supports Google Trends RSS, optional YouTube Data API, optional Reddit API,
and manual/exported social listening CSV imports. TikTok is recorded as an
access-gated source until Research API credentials/approval are available.
"""

from __future__ import annotations

import argparse
import base64
import csv
import datetime as dt
import email.utils
import hashlib
import json
import os
import re
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TZ = dt.timezone(dt.timedelta(hours=7))
GT_NS = {"ht": "https://trends.google.com/trending/rss"}
SOCIAL_IMPORT_DIR = ROOT / "data" / "social_media_imports"

SIGNAL_PREFIX = {
    "google_trends": "gt",
    "youtube": "yt",
    "reddit": "rd",
    "tiktok": "tk",
    "instagram": "ig",
    "facebook": "fb",
    "twitter": "tw",
    "x": "x",
    "threads": "thd",
    "manual_social": "ms",
}

CSV_FIELDS = {
    "viral_signal_intelligence.csv": [
        "signal_id",
        "captured_at",
        "platform",
        "source_type",
        "source_url",
        "topic",
        "summary_th",
        "people_involved_type",
        "harm_level",
        "verification_status",
        "virality_evidence",
        "engagement_snapshot",
        "trend_age_hours",
        "demand_window",
        "audience_need",
        "candidate_product_category",
        "candidate_query",
        "ethics_color",
        "policy_risk",
        "claim_risk",
        "human_review_required",
        "product_mapping_status",
        "notes_th",
    ],
    "signal_observations.csv": [
        "observation_id",
        "signal_id",
        "observed_at",
        "views",
        "likes",
        "comments",
        "shares",
        "saves",
        "search_rank",
        "trend_rank",
        "velocity_1h",
        "velocity_6h",
        "sentiment_th",
        "comment_themes_th",
        "raw_snapshot_json",
        "observer_agent",
    ],
    "signal_clusters.csv": [
        "cluster_id",
        "cluster_key",
        "normalized_topic_th",
        "first_seen_at",
        "last_seen_at",
        "lead_signal_id",
        "source_count",
        "platform_count",
        "max_signal_score",
        "ethics_color_max",
        "cluster_status",
        "recommended_need_th",
        "blocked_reason_th",
    ],
    "product_need_map.csv": [
        "need_id",
        "cluster_id",
        "audience_need_th",
        "safe_angle_th",
        "unsafe_angle_th",
        "product_category",
        "shopee_query",
        "claim_limits_th",
        "ethics_gate",
        "mapping_confidence",
        "mapping_status",
        "reviewer",
    ],
    "marketing_collection.csv": [
        "collection_id",
        "created_at",
        "updated_at",
        "owner_team",
        "selected_by",
        "selection_source",
        "signal_id",
        "cluster_id",
        "need_id",
        "product_idea_th",
        "product_category",
        "shopee_query",
        "marketing_angle_th",
        "buyer_archetype_th",
        "hook_hypothesis_th",
        "why_marketing_selected_th",
        "priority",
        "expected_content_format",
        "ethics_color_initial",
        "policy_risk_initial",
        "claim_risk_initial",
        "research_status",
        "research_owner",
        "candidate_record_id",
        "collection_status",
        "notes_th",
    ],
    "human_review_inbox.csv": [
        "review_id",
        "created_at",
        "review_type",
        "ethics_color",
        "source_ref",
        "signal_id",
        "product_candidate_id",
        "question_th",
        "recommended_decision",
        "decision",
        "decided_at",
        "decided_by",
        "decision_notes_th",
    ],
    "subagent_ops_queue.csv": [
        "task_id",
        "created_at",
        "updated_at",
        "owner_team",
        "owner_agent",
        "stage",
        "status",
        "priority",
        "source_ref",
        "signal_id",
        "cluster_id",
        "product_candidate_id",
        "summary_th",
        "next_action",
        "next_retry_at",
        "retry_count",
        "last_error",
        "human_action_needed",
        "notes_th",
    ],
}

SENSITIVE_AMBER = [
    "การเมือง",
    "นายก",
    "รัฐบาล",
    "ศาล",
    "คดี",
    "หุ้น",
    "ทอง",
    "ราคา",
    "สงคราม",
    "กัมพูชา",
    "ฮุน",
    "โรค",
    "ไข้",
    "วัคซีน",
    "หวย",
    "lottery",
    "scratch-off",
    "scratch",
    "politics",
    "court",
    "legal",
    "settlement",
    "privacy",
    "legislation",
    "gold price",
    "energy costs",
    "stock",
    "corporation",
    "ex husband",
    "celebrity",
]

SENSITIVE_RED = [
    "ตาย",
    "เสียชีวิต",
    "ฆ่า",
    "ทำร้าย",
    "อุบัติเหตุ",
    "เด็กหาย",
    "ข่มขืน",
    "เหยื่อ",
    "เลือด",
    "death",
    "cause of death",
    "murder",
    "suicide",
    "killed",
    "victim",
    "dead",
    "overcrowded migrant",
]

MAPPING_RULES = [
    {
        "keywords": ["ฝน", "พายุ", "น้ำท่วม", "สภาพอากาศ", "อากาศ", "weather", "rain", "storm"],
        "category": "rain_gear",
        "query": "site:shopee.co.th เสื้อกันฝนพกพา rain cover dry bag",
        "need": "เตรียมของกันฝนแบบพกง่ายสำหรับเดินทาง",
        "angle": "ฝนมาไวแต่ยังเดินทางต่อได้แบบไม่ดราม่า",
        "unsafe": "ขายบนภาพภัยพิบัติหรือรับประกันกันน้ำทุกสถานการณ์",
        "claim": "ห้ามรับประกันกันน้ำสมบูรณ์หรือใช้ภาพน้ำท่วมรุนแรง",
    },
    {
        "keywords": ["เปิดเทอม", "โรงเรียน", "นักเรียน"],
        "category": "back_to_school",
        "query": "site:shopee.co.th สติกเกอร์ชื่อกันน้ำ กล่องข้าว กระเป๋านักเรียน",
        "need": "เตรียมของเปิดเทอมที่หาเจอง่ายและทนชีวิตประจำวัน",
        "angle": "เปิดเทอมของต้องพร้อมและไม่หายง่าย",
        "unsafe": "ใช้ข้อมูลเด็กส่วนตัวหรืออ้างราคาลดจริงโดยไม่ตรวจ",
        "claim": "ห้ามใช้ข้อมูลเด็กส่วนตัวและต้องตรวจราคา/SKU ก่อน CTA",
    },
    {
        "keywords": ["ร้อน", "อากาศร้อน", "แดด"],
        "category": "portable_cooling",
        "query": "site:shopee.co.th พัดลมพกพา หมวกกันแดด ผ้าเย็น",
        "need": "รับมืออากาศร้อนเมื่อต้องออกไปข้างนอก",
        "angle": "พกของเบาเพื่อให้วัน outdoor สบายขึ้น",
        "unsafe": "เคลมลดความร้อนร่างกายหรือป้องกันลมแดดแน่นอน",
        "claim": "ใช้แค่ comfort claim ไม่ใช่ medical/safety claim",
    },
    {
        "keywords": ["คอนเสิร์ต", "festival", "pride", "งาน", "อีเวนต์"],
        "category": "event_comfort",
        "query": "site:shopee.co.th พัดลมพกพา กระเป๋าใส clear bag event",
        "need": "พกของเบาในงานกลางแจ้งและงานคนเยอะ",
        "angle": "ออกงานทั้งวันแบบไม่รกมือ",
        "unsafe": "ใช้ identity เป็น gimmick หรือใช้ likeness คนจริง",
        "claim": "ต้องเคารพ community และห้าม implied endorsement",
    },
    {
        "keywords": ["มือถือ", "iphone", "android"],
        "category": "phone_accessory",
        "query": "site:shopee.co.th ซองกันน้ำมือถือ สายคล้องมือถือ power bank",
        "need": "มือถือยังต้องใช้ระหว่างเดินทางหรือออกงาน",
        "angle": "หยิบใช้ได้ไวเมื่อฝนเริ่มหรือแบตใกล้หมด",
        "unsafe": "รับประกันมือถือปลอดภัยหรือกันน้ำทุกกรณี",
        "claim": "ห้ามรับประกันป้องกันความเสียหายแน่นอน",
    },
    {
        "keywords": ["บอล", "ฟุตบอล", "กีฬา", "lpga", "golf", "cricket", "vs", "พบ"],
        "category": "fan_gear",
        "query": "site:shopee.co.th เสื้อกีฬา ผ้าพันคอ เชียร์บอล ของดูบอล",
        "need": "ของดูบอลและเชียร์กีฬาที่ใช้ซ้ำได้",
        "angle": "จัดมุมดูบอลที่บ้านหรือของพกไปเชียร์",
        "unsafe": "ใช้โลโก้ทีม/ลิขสิทธิ์โดยไม่ได้สิทธิ์",
        "claim": "ต้องเลี่ยง IP/logo/team kit ปลอม",
    },
]


def now_bkk() -> str:
    return dt.datetime.now(TZ).replace(microsecond=0).isoformat()


def compact_now() -> str:
    return dt.datetime.now(TZ).strftime("%Y%m%d%H%M%S")


def slug_hash(text: str) -> str:
    cleaned = re.sub(r"\s+", "-", text.strip().lower())
    cleaned = re.sub(r"[^0-9a-zA-Zก-๙_-]+", "", cleaned)
    cleaned = cleaned.strip("-")[:40] or "trend"
    digest = hashlib.sha1(text.encode("utf-8")).hexdigest()[:8]
    return f"{cleaned}-{digest}"


def read_csv(name: str) -> list[dict[str, str]]:
    path = ROOT / "data" / name
    fields = CSV_FIELDS[name]
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        write_csv(name, [])
        return []
    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames != fields:
            raise SystemExit(f"Unexpected header for {path}: {reader.fieldnames}")
        return [{k: (v or "") for k, v in row.items() if k is not None} for row in reader]


def write_csv(name: str, rows: list[dict[str, str]]) -> None:
    path = ROOT / "data" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = CSV_FIELDS[name]
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def append_unique(name: str, rows: list[dict[str, str]], key: str, row: dict[str, str]) -> bool:
    existing = {r.get(key, "") for r in rows}
    if row.get(key, "") in existing:
        return False
    rows.append(row)
    return True


def fetch_google_trends(geo: str, limit: int) -> list[dict[str, object]]:
    url = f"https://trends.google.com/trending/rss?geo={geo}"
    req = urllib.request.Request(url, headers={"User-Agent": "AutoAffiSocialScanner/0.1"})
    with urllib.request.urlopen(req, timeout=25) as response:
        xml = response.read()
    root = ET.fromstring(xml)
    items = []
    for rank, item in enumerate(root.findall("./channel/item")[:limit], start=1):
        title = item.findtext("title") or ""
        pub_date = item.findtext("pubDate") or ""
        approx = item.findtext("ht:approx_traffic", default="", namespaces=GT_NS)
        news = []
        for news_item in item.findall("ht:news_item", GT_NS):
            news.append(
                {
                    "title": news_item.findtext("ht:news_item_title", default="", namespaces=GT_NS),
                    "url": news_item.findtext("ht:news_item_url", default="", namespaces=GT_NS),
                    "source": news_item.findtext("ht:news_item_source", default="", namespaces=GT_NS),
                }
            )
        items.append({"geo": geo, "rank": rank, "title": title, "pub_date": pub_date, "approx": approx, "news": news})
    return items


def fetch_json(url: str, *, headers: dict[str, str] | None = None, data: bytes | None = None, timeout: int = 25) -> dict:
    req = urllib.request.Request(url, data=data, headers=headers or {})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def source_issue_task_id(source_id: str) -> str:
    return "task-source-access-" + re.sub(r"[^a-z0-9_-]+", "-", source_id.lower()).strip("-")


def upsert_source_issue(
    tasks: list[dict[str, str]],
    *,
    run_at: str,
    source_id: str,
    summary_th: str,
    next_action: str,
    last_error: str = "",
) -> None:
    task_id = source_issue_task_id(source_id)
    row = next((r for r in tasks if r.get("task_id") == task_id), None)
    payload = {
        "task_id": task_id,
        "created_at": run_at,
        "updated_at": run_at,
        "owner_team": "social_radar",
        "owner_agent": "source_access_manager",
        "stage": "source_access",
        "status": "blocked",
        "priority": "medium",
        "source_ref": source_id,
        "signal_id": "",
        "cluster_id": "",
        "product_candidate_id": "",
        "summary_th": summary_th,
        "next_action": next_action,
        "next_retry_at": "",
        "retry_count": "0",
        "last_error": last_error,
        "human_action_needed": "yes",
        "notes_th": "official/API/manual route only; do not scrape around platform controls",
    }
    if row:
        created_at = row.get("created_at") or run_at
        row.update(payload)
        row["created_at"] = created_at
    else:
        tasks.append(payload)


def google_trends_items(geo: str, limit: int) -> list[dict[str, object]]:
    items: list[dict[str, object]] = []
    for item in fetch_google_trends(geo, limit):
        news = item["news"]  # type: ignore[assignment]
        source_url = ""
        source_names = []
        related_titles = []
        for news_item in news:  # type: ignore[union-attr]
            if not source_url and news_item.get("url"):
                source_url = str(news_item["url"])
            if news_item.get("source"):
                source_names.append(str(news_item["source"]))
            if news_item.get("title"):
                related_titles.append(str(news_item["title"]))
        items.append(
            {
                "platform": "google_trends",
                "source_type": "social_search_trend",
                "geo": geo.upper(),
                "rank": int(item["rank"]),
                "title": str(item["title"]),
                "pub_date": str(item["pub_date"]),
                "traffic": str(item["approx"]),
                "source_url": source_url or f"https://trends.google.com/trending?geo={geo.upper()}",
                "source_names": source_names,
                "related_titles": related_titles,
                "engagement": {},
                "demand_window": "4-48h" if geo.upper() == "TH" else "24-72h",
                "observer_agent": "social_media_scanner_google_trends",
                "virality_evidence": f"Google Trends RSS geo={geo.upper()} rank={item['rank']} approx_traffic={item['approx']}",
                "report_label": f"{geo.upper()} #{item['rank']}",
            }
        )
    return items


def youtube_items(geos: list[str], limit: int, tasks: list[dict[str, str]], run_at: str) -> list[dict[str, object]]:
    api_key = os.getenv("YOUTUBE_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        upsert_source_issue(
            tasks,
            run_at=run_at,
            source_id="youtube_data_api",
            summary_th="YouTube social-video scan ยังไม่มี YOUTUBE_API_KEY/GOOGLE_API_KEY",
            next_action="add_official_youtube_data_api_key_or_disable_source",
        )
        return []

    results: list[dict[str, object]] = []
    for geo in dict.fromkeys(g.upper() for g in geos):
        params = urllib.parse.urlencode(
            {
                "part": "snippet,statistics",
                "chart": "mostPopular",
                "regionCode": geo,
                "maxResults": str(min(limit, 50)),
                "key": api_key,
            }
        )
        url = f"https://www.googleapis.com/youtube/v3/videos?{params}"
        try:
            data = fetch_json(url, headers={"User-Agent": "AutoAffiSocialScanner/0.1"})
        except Exception as exc:
            upsert_source_issue(
                tasks,
                run_at=run_at,
                source_id="youtube_data_api",
                summary_th=f"YouTube Data API scan ล้มเหลวสำหรับ region {geo}",
                next_action="check_api_key_quota_region_and_api_enablement",
                last_error=str(exc)[:300],
            )
            continue

        for rank, video in enumerate(data.get("items", [])[:limit], start=1):
            snippet = video.get("snippet", {})
            stats = video.get("statistics", {})
            title = str(snippet.get("title") or "").strip()
            video_id = str(video.get("id") or "")
            if not title or not video_id:
                continue
            results.append(
                {
                    "platform": "youtube",
                    "source_type": "social_video_trending",
                    "geo": geo,
                    "rank": rank,
                    "title": title,
                    "pub_date": str(snippet.get("publishedAt") or ""),
                    "traffic": str(stats.get("viewCount") or ""),
                    "source_url": f"https://www.youtube.com/watch?v={video_id}",
                    "source_names": [str(snippet.get("channelTitle") or "YouTube")],
                    "related_titles": [str(snippet.get("description") or "")[:500]],
                    "engagement": {
                        "views": str(stats.get("viewCount") or ""),
                        "likes": str(stats.get("likeCount") or ""),
                        "comments": str(stats.get("commentCount") or ""),
                    },
                    "demand_window": "24-72h",
                    "observer_agent": "social_media_scanner_youtube_api",
                    "virality_evidence": f"YouTube mostPopular region={geo} rank={rank} views={stats.get('viewCount', '')}",
                    "report_label": f"YouTube {geo} #{rank}",
                }
            )
    return results


def reddit_access_token(client_id: str, client_secret: str, user_agent: str) -> str:
    auth = base64.b64encode(f"{client_id}:{client_secret}".encode("utf-8")).decode("ascii")
    body = urllib.parse.urlencode({"grant_type": "client_credentials"}).encode("utf-8")
    data = fetch_json(
        "https://www.reddit.com/api/v1/access_token",
        headers={
            "Authorization": f"Basic {auth}",
            "User-Agent": user_agent,
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data=body,
    )
    return str(data.get("access_token") or "")


def reddit_items(limit: int, tasks: list[dict[str, str]], run_at: str) -> list[dict[str, object]]:
    client_id = os.getenv("REDDIT_CLIENT_ID")
    client_secret = os.getenv("REDDIT_CLIENT_SECRET")
    user_agent = os.getenv("REDDIT_USER_AGENT") or "AutoAffiSocialScanner/0.1 by local-codex"
    if not client_id or not client_secret:
        upsert_source_issue(
            tasks,
            run_at=run_at,
            source_id="reddit_api",
            summary_th="Reddit social-discussion scan ยังไม่มี REDDIT_CLIENT_ID/REDDIT_CLIENT_SECRET",
            next_action="add_official_reddit_api_credentials_or_keep_manual_review",
        )
        return []

    try:
        token = reddit_access_token(client_id, client_secret, user_agent)
        if not token:
            raise RuntimeError("empty access token")
        params = urllib.parse.urlencode({"limit": str(min(limit, 50))})
        data = fetch_json(
            f"https://oauth.reddit.com/r/popular/hot?{params}",
            headers={"Authorization": f"Bearer {token}", "User-Agent": user_agent},
        )
    except Exception as exc:
        upsert_source_issue(
            tasks,
            run_at=run_at,
            source_id="reddit_api",
            summary_th="Reddit API scan ล้มเหลว",
            next_action="check_reddit_credentials_user_agent_and_app_permissions",
            last_error=str(exc)[:300],
        )
        return []

    results: list[dict[str, object]] = []
    children = data.get("data", {}).get("children", [])
    for rank, child in enumerate(children[:limit], start=1):
        post = child.get("data", {})
        title = str(post.get("title") or "").strip()
        if not title:
            continue
        permalink = str(post.get("permalink") or "")
        results.append(
            {
                "platform": "reddit",
                "source_type": "social_discussion_hot",
                "geo": "GLOBAL",
                "rank": rank,
                "title": title,
                "pub_date": "",
                "traffic": str(post.get("score") or post.get("ups") or ""),
                "source_url": f"https://www.reddit.com{permalink}" if permalink else str(post.get("url") or ""),
                "source_names": [f"r/{post.get('subreddit', 'popular')}"],
                "related_titles": [str(post.get("selftext") or "")[:500]],
                "engagement": {
                    "likes": str(post.get("score") or post.get("ups") or ""),
                    "comments": str(post.get("num_comments") or ""),
                },
                "demand_window": "24-72h",
                "observer_agent": "social_media_scanner_reddit_api",
                "virality_evidence": f"Reddit r/popular hot rank={rank} score={post.get('score', '')} comments={post.get('num_comments', '')}",
                "report_label": f"Reddit GLOBAL #{rank}",
            }
        )
    return results


def manual_social_import_items(limit: int) -> list[dict[str, object]]:
    if not SOCIAL_IMPORT_DIR.exists():
        return []

    results: list[dict[str, object]] = []
    for path in sorted(SOCIAL_IMPORT_DIR.glob("*.csv")):
        with path.open(newline="", encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            for row_number, row in enumerate(reader, start=1):
                title = (row.get("title") or row.get("topic") or "").strip()
                if not title:
                    continue
                platform = (row.get("platform") or "manual_social").strip().lower() or "manual_social"
                geo = (row.get("country") or row.get("geo") or row.get("region") or "TH").strip().upper()
                engagement = {
                    "views": row.get("views", ""),
                    "likes": row.get("likes", ""),
                    "comments": row.get("comments", ""),
                    "shares": row.get("shares", ""),
                    "saves": row.get("saves", ""),
                }
                traffic = row.get("views") or row.get("likes") or row.get("shares") or ""
                results.append(
                    {
                        "platform": platform if platform in SIGNAL_PREFIX else "manual_social",
                        "source_type": row.get("source_type") or "manual_social_import",
                        "geo": geo,
                        "rank": len(results) + 1,
                        "title": title,
                        "pub_date": row.get("published_at") or row.get("observed_at") or "",
                        "traffic": traffic,
                        "source_url": row.get("url") or row.get("source_url") or "",
                        "source_names": [row.get("creator") or row.get("channel") or path.name],
                        "related_titles": [row.get("notes") or row.get("description") or ""],
                        "engagement": engagement,
                        "demand_window": row.get("demand_window") or "manual-review",
                        "observer_agent": "social_media_scanner_manual_import",
                        "virality_evidence": row.get("virality_evidence")
                        or f"manual social import file={path.name} row={row_number} traffic={traffic}",
                        "report_label": f"Manual {geo} #{len(results) + 1}",
                    }
                )
                if len(results) >= limit:
                    return results
    return results


def tiktok_access_issue(tasks: list[dict[str, str]], run_at: str) -> None:
    if os.getenv("TIKTOK_RESEARCH_ACCESS_TOKEN"):
        upsert_source_issue(
            tasks,
            run_at=run_at,
            source_id="tiktok_research_api",
            summary_th="พบ TikTok token แล้ว แต่ adapter ยังต้อง lock fields/query policy ก่อนเปิดใช้",
            next_action="implement_tiktok_research_api_adapter_after_schema_review",
        )
        return
    upsert_source_issue(
        tasks,
        run_at=run_at,
        source_id="tiktok_research_api",
        summary_th="TikTok scan ต้องใช้ Research API approval/token หรือ manual export",
        next_action="request_tiktok_research_api_access_or_add_manual_social_import_csv",
    )


def pub_age_hours(pub_date: str) -> str:
    try:
        parsed = email.utils.parsedate_to_datetime(pub_date)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=dt.timezone.utc)
        delta = dt.datetime.now(dt.timezone.utc) - parsed.astimezone(dt.timezone.utc)
        return str(max(0, int(delta.total_seconds() // 3600)))
    except Exception:
        return ""


def classify(title: str, news_titles: list[str]) -> tuple[str, str, str, str]:
    text = " ".join([title, *news_titles]).lower()
    if any(k.lower() in text for k in SENSITIVE_RED):
        return "red", "high", "high", "private_person_or_victim"
    if any(k.lower() in text for k in SENSITIVE_AMBER):
        return "amber", "medium", "medium", "public_or_sensitive_topic"
    return "green", "low", "low", "none"


def product_mapping(title: str) -> dict[str, str] | None:
    lower = title.lower()
    for rule in MAPPING_RULES:
        if any(keyword.lower() in lower for keyword in rule["keywords"]):
            return rule
    return None


def signal_score(ethics: str, traffic: str, rank: int, has_mapping: bool) -> str:
    score = 50
    digits = re.sub(r"\D", "", traffic or "")
    if digits:
        score += min(25, int(digits) // 1000)
    score += max(0, 15 - rank)
    if has_mapping:
        score += 8
    if ethics == "amber":
        score -= 18
    if ethics == "red":
        score = 0
    return str(max(0, min(100, score)))


def process_source_items(
    source_items: list[dict[str, object]],
    *,
    run_at: str,
    run_key: str,
    write_marketing: bool,
    signals: list[dict[str, str]],
    observations: list[dict[str, str]],
    clusters: list[dict[str, str]],
    needs: list[dict[str, str]],
    collections: list[dict[str, str]],
    reviews: list[dict[str, str]],
    tasks: list[dict[str, str]],
) -> tuple[int, int, int, list[str]]:
    signal_index = {r["signal_id"]: r for r in signals}
    cluster_index = {r["cluster_id"]: r for r in clusters}
    added_signals = 0
    added_observations = 0
    added_collections = 0
    seen_report: list[str] = []

    for item in source_items:
        title = str(item.get("title") or "").strip()
        if not title:
            continue
        platform = str(item.get("platform") or "manual_social").strip().lower()
        source_type = str(item.get("source_type") or "social_signal")
        geo = str(item.get("geo") or "GLOBAL").upper()
        rank = int(item.get("rank") or 99)
        traffic = str(item.get("traffic") or "")
        source_url = str(item.get("source_url") or "")
        source_names = [str(v) for v in item.get("source_names", [])]  # type: ignore[arg-type]
        related_titles = [str(v) for v in item.get("related_titles", [])]  # type: ignore[arg-type]
        engagement = item.get("engagement", {})
        if not isinstance(engagement, dict):
            engagement = {}

        prefix = SIGNAL_PREFIX.get(platform, "ms")
        signal_id = str(item.get("signal_id") or f"{prefix}-{geo.lower()}-{slug_hash(title)}")
        cluster_id = f"cluster-{signal_id}"
        need_id = f"need-{signal_id}"
        ethics, policy_risk, claim_risk, people_type = classify(title, related_titles)
        mapping = product_mapping(title)
        score = signal_score(ethics, traffic, rank, mapping is not None)
        age = str(item.get("trend_age_hours") or pub_age_hours(str(item.get("pub_date") or "")))
        first_seen = signal_index.get(signal_id, {}).get("captured_at", run_at)

        signal_row = {
            "signal_id": signal_id,
            "captured_at": first_seen,
            "platform": platform,
            "source_type": source_type,
            "source_url": source_url,
            "topic": title,
            "summary_th": str(item.get("summary_th") or f"{platform} {geo} พบสัญญาณไวรัล '{title}' traffic/engagement {traffic}"),
            "people_involved_type": people_type,
            "harm_level": "high" if ethics == "red" else ("medium" if ethics == "amber" else "low"),
            "verification_status": "source_seen",
            "virality_evidence": str(item.get("virality_evidence") or f"{platform} rank={rank} traffic={traffic}"),
            "engagement_snapshot": json.dumps(
                {"geo": geo, "rank": rank, "traffic": traffic, "sources": source_names[:3], "engagement": engagement},
                ensure_ascii=False,
            ),
            "trend_age_hours": age,
            "demand_window": str(item.get("demand_window") or "24-72h"),
            "audience_need": mapping["need"] if mapping else "ต้องให้ Marketing/Research ตีความ need ก่อน",
            "candidate_product_category": mapping["category"] if mapping else "no_direct_product_mapping",
            "candidate_query": mapping["query"] if mapping else "",
            "ethics_color": ethics,
            "policy_risk": policy_risk,
            "claim_risk": claim_risk,
            "human_review_required": "yes" if ethics != "green" or not mapping else "no",
            "product_mapping_status": "need_identified" if mapping and ethics != "red" else ("red_no_product_mapping" if ethics == "red" else "needs_verification"),
            "notes_th": f"{source_type} from {platform}; repeat sightings update observations and cluster velocity",
        }
        if signal_id not in signal_index:
            signals.append(signal_row)
            signal_index[signal_id] = signal_row
            added_signals += 1
        else:
            existing = signal_index[signal_id]
            preserved_captured_at = existing.get("captured_at") or first_seen
            existing.update(signal_row)
            existing["captured_at"] = preserved_captured_at

        observation = {
            "observation_id": f"obs-{signal_id}-{run_key}",
            "signal_id": signal_id,
            "observed_at": run_at,
            "views": str(engagement.get("views") or ""),
            "likes": str(engagement.get("likes") or ""),
            "comments": str(engagement.get("comments") or ""),
            "shares": str(engagement.get("shares") or ""),
            "saves": str(engagement.get("saves") or ""),
            "search_rank": str(rank) if platform == "google_trends" else "",
            "trend_rank": str(rank),
            "velocity_1h": traffic,
            "velocity_6h": traffic,
            "sentiment_th": "unknown",
            "comment_themes_th": f"source trend: {title}",
            "raw_snapshot_json": json.dumps(item, ensure_ascii=False, default=str),
            "observer_agent": str(item.get("observer_agent") or f"social_media_scanner_{platform}"),
        }
        if append_unique("signal_observations.csv", observations, "observation_id", observation):
            added_observations += 1

        if cluster_id in cluster_index:
            row = cluster_index[cluster_id]
            row["last_seen_at"] = run_at
            row["max_signal_score"] = str(max(int(row.get("max_signal_score") or 0), int(score)))
            row["cluster_status"] = "marketing_ready" if mapping and ethics == "green" else ("needs_human_review" if ethics == "amber" else "blocked")
        else:
            cluster_row = {
                "cluster_id": cluster_id,
                "cluster_key": signal_id,
                "normalized_topic_th": title,
                "first_seen_at": run_at,
                "last_seen_at": run_at,
                "lead_signal_id": signal_id,
                "source_count": str(max(1, len(source_names))),
                "platform_count": "1",
                "max_signal_score": score,
                "ethics_color_max": ethics,
                "cluster_status": "marketing_ready" if mapping and ethics == "green" else ("needs_human_review" if ethics == "amber" else "blocked"),
                "recommended_need_th": mapping["need"] if mapping else "",
                "blocked_reason_th": "red sensitive trend" if ethics == "red" else "",
            }
            clusters.append(cluster_row)
            cluster_index[cluster_id] = cluster_row

        if mapping and not any(r["need_id"] == need_id for r in needs):
            needs.append(
                {
                    "need_id": need_id,
                    "cluster_id": cluster_id,
                    "audience_need_th": mapping["need"],
                    "safe_angle_th": mapping["angle"],
                    "unsafe_angle_th": mapping["unsafe"],
                    "product_category": mapping["category"],
                    "shopee_query": mapping["query"],
                    "claim_limits_th": mapping["claim"],
                    "ethics_gate": ethics,
                    "mapping_confidence": "70" if ethics == "green" else "45",
                    "mapping_status": "query_ready" if ethics == "green" else "needs_human_review",
                    "reviewer": "",
                }
            )

        if write_marketing and mapping and ethics != "red":
            collection_id = f"mc-{signal_id}"
            if not any(r["collection_id"] == collection_id for r in collections):
                collections.append(
                    {
                        "collection_id": collection_id,
                        "created_at": run_at,
                        "updated_at": run_at,
                        "owner_team": "marketing",
                        "selected_by": "social_media_scanner",
                        "selection_source": source_type,
                        "signal_id": signal_id,
                        "cluster_id": cluster_id,
                        "need_id": need_id,
                        "product_idea_th": mapping["category"],
                        "product_category": mapping["category"],
                        "shopee_query": mapping["query"],
                        "marketing_angle_th": mapping["angle"],
                        "buyer_archetype_th": "ผู้ใช้ไทยที่กำลังสนใจ trend นี้และมี pain ใช้งานจริง",
                        "hook_hypothesis_th": f"เปิดด้วย trend '{title}' แล้วโยงเป็น use case ที่ไม่ overclaim",
                        "why_marketing_selected_th": f"{platform} {geo} rank {rank} traffic/engagement {traffic} ทำให้เห็น attention ซ้ำได้",
                        "priority": "high" if ethics == "green" and int(score) >= 70 else "medium",
                        "expected_content_format": "15s_hook_test",
                        "ethics_color_initial": ethics,
                        "policy_risk_initial": policy_risk,
                        "claim_risk_initial": claim_risk,
                        "research_status": "needs_research" if ethics == "green" else "needs_human_review",
                        "research_owner": "product_research",
                        "candidate_record_id": "",
                        "collection_status": "selected_for_research",
                        "notes_th": f"auto-selected from {platform}; Research must validate before candidate",
                    }
                )
                added_collections += 1

            task_id = f"task-research-{collection_id}"
            if not any(r["task_id"] == task_id for r in tasks):
                tasks.append(
                    {
                        "task_id": task_id,
                        "created_at": run_at,
                        "updated_at": run_at,
                        "owner_team": "product_research",
                        "owner_agent": "research_validation_sweep",
                        "stage": "research_validation",
                        "status": "queued",
                        "priority": "high" if ethics == "green" else "medium",
                        "source_ref": collection_id,
                        "signal_id": signal_id,
                        "cluster_id": cluster_id,
                        "product_candidate_id": "",
                        "summary_th": f"Research validate {mapping['category']} from {platform} topic {title}",
                        "next_action": "validate_shopee_product_evidence",
                        "next_retry_at": "",
                        "retry_count": "0",
                        "last_error": "",
                        "human_action_needed": "yes" if ethics != "green" else "no",
                        "notes_th": mapping["claim"],
                    }
                )

        if ethics != "green":
            review_id = f"review-{signal_id}"
            if not any(r["review_id"] == review_id for r in reviews):
                reviews.append(
                    {
                        "review_id": review_id,
                        "created_at": run_at,
                        "review_type": "social_trend_safety_review",
                        "ethics_color": ethics,
                        "source_ref": signal_id,
                        "signal_id": signal_id,
                        "product_candidate_id": "",
                        "question_th": f"ควรใช้ trend '{title}' เป็น marketing signal หรือ archive เท่านั้น?",
                        "recommended_decision": "approve_generalized_need_only" if mapping and ethics == "amber" else "reject_product_mapping",
                        "decision": "",
                        "decided_at": "",
                        "decided_by": "",
                        "decision_notes_th": "",
                    }
                )

        seen_report.append(
            f"- {item.get('report_label') or platform + ' ' + geo + ' #' + str(rank)}: {title} ({traffic}) -> {ethics} / {mapping['category'] if mapping else 'no mapping'}"
        )

    return added_signals, added_observations, added_collections, seen_report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--geo", action="append", default=None, help="Google Trends geo code. Repeatable.")
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--write-marketing", action="store_true")
    parser.add_argument("--report", action="store_true")
    parser.add_argument("--skip-youtube", action="store_true", help="Do not attempt the YouTube Data API adapter.")
    parser.add_argument("--skip-reddit", action="store_true", help="Do not attempt the Reddit API adapter.")
    parser.add_argument("--skip-tiktok-issue", action="store_true", help="Do not record TikTok access-gate tasks.")
    parser.add_argument("--skip-manual-imports", action="store_true", help="Do not ingest data/social_media_imports/*.csv.")
    args = parser.parse_args()

    run_at = now_bkk()
    run_key = compact_now()
    signals = read_csv("viral_signal_intelligence.csv")
    observations = read_csv("signal_observations.csv")
    clusters = read_csv("signal_clusters.csv")
    needs = read_csv("product_need_map.csv")
    collections = read_csv("marketing_collection.csv")
    reviews = read_csv("human_review_inbox.csv")
    tasks = read_csv("subagent_ops_queue.csv")

    geos = args.geo or ["TH"]
    normalized_geos = list(dict.fromkeys(g.upper() for g in geos))
    source_items: list[dict[str, object]] = []
    for geo in dict.fromkeys(g.upper() for g in geos):
        source_items.extend(google_trends_items(geo.upper(), args.limit))
    if not args.skip_youtube:
        source_items.extend(youtube_items(normalized_geos, args.limit, tasks, run_at))
    if not args.skip_reddit:
        source_items.extend(reddit_items(args.limit, tasks, run_at))
    if not args.skip_tiktok_issue:
        tiktok_access_issue(tasks, run_at)
    if not args.skip_manual_imports:
        source_items.extend(manual_social_import_items(args.limit))

    added_signals, added_observations, added_collections, seen_report = process_source_items(
        source_items,
        run_at=run_at,
        run_key=run_key,
        write_marketing=args.write_marketing,
        signals=signals,
        observations=observations,
        clusters=clusters,
        needs=needs,
        collections=collections,
        reviews=reviews,
        tasks=tasks,
    )

    write_csv("viral_signal_intelligence.csv", signals)
    write_csv("signal_observations.csv", observations)
    write_csv("signal_clusters.csv", clusters)
    write_csv("product_need_map.csv", needs)
    write_csv("marketing_collection.csv", collections)
    write_csv("human_review_inbox.csv", reviews)
    write_csv("subagent_ops_queue.csv", tasks)

    if args.report:
        report_dir = ROOT / "reports"
        report_dir.mkdir(exist_ok=True)
        report_path = report_dir / f"social_scan_{dt.datetime.now(TZ).strftime('%Y-%m-%d')}.md"
        report_path.write_text(
            "# Social Media Scanner Report\n\n"
            f"Run at: `{run_at}`\n\n"
            f"- New signals: {added_signals}\n"
            f"- Observations: {added_observations}\n"
            f"- New marketing rows: {added_collections}\n"
            f"- Source items scanned: {len(source_items)}\n\n"
            "## Seen Signals\n\n"
            + "\n".join(seen_report)
            + "\n",
            encoding="utf-8",
        )
        print(report_path)

    print(
        json.dumps(
            {
                "run_at": run_at,
                "new_signals": added_signals,
                "observations": added_observations,
                "new_marketing_rows": added_collections,
                "source_items_scanned": len(source_items),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
