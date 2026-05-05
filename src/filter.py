from __future__ import annotations

from src.fetch import Article


def dedupe_articles(articles: list[Article]) -> list[Article]:
    seen: set[str] = set()
    unique: list[Article] = []

    for article in articles:
        key = article.link or article.title.lower()
        if key in seen:
            continue
        seen.add(key)
        unique.append(article)

    return unique
