from datetime import datetime, timezone

import feedparser


NEWS_FEEDS: dict[str, str] = {
    "Lenta": "https://lenta.ru/rss",
    "RBC": "https://rssexport.rbc.ru/rbcnews/news/30/full.rss",
    "RIA": "https://ria.ru/export/rss2/archive/index.xml",
}


def _entry_datetime_iso(entry: dict) -> str:
    if "published_parsed" in entry and entry.published_parsed:
        dt = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
        return dt.isoformat()
    return datetime.now(timezone.utc).isoformat()


def fetch_news(limit_per_source: int = 100) -> list[dict]:
    items: list[dict] = []
    for source, url in NEWS_FEEDS.items():
        feed = feedparser.parse(url)
        for entry in feed.entries[:limit_per_source]:
            title = (entry.get("title") or "").strip()
            link = (entry.get("link") or "").strip()
            summary = (entry.get("summary") or entry.get("description") or "").strip()

            if not title or not link:
                continue

            items.append(
                {
                    "title": title,
                    "summary": summary,
                    "link": link,
                    "published_at": _entry_datetime_iso(entry),
                    "source": source,
                }
            )
    return items
