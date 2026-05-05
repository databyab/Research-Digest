from __future__ import annotations

from dataclasses import dataclass
from html import unescape
from typing import Iterable

import feedparser


@dataclass(frozen=True)
class Article:
    title: str
    link: str
    summary: str
    published: str


def fetch_articles(feed_urls: Iterable[str], max_items: int) -> list[Article]:
    articles: list[Article] = []

    for feed_url in feed_urls:
        feed = feedparser.parse(feed_url)
        if getattr(feed, "bozo", False):
            continue

        for entry in feed.entries:
            articles.append(
                Article(
                    title=unescape(getattr(entry, "title", "Untitled")).strip(),
                    link=getattr(entry, "link", "").strip(),
                    summary=unescape(getattr(entry, "summary", "")).strip(),
                    published=getattr(entry, "published", "Unknown date").strip(),
                )
            )

    return articles[:max_items]
