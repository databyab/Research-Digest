from __future__ import annotations

from datetime import date

from config.settings import ROOT_DIR, get_settings
from src.emailer import send_email
from src.fetch import fetch_articles
from src.filter import dedupe_articles
from src.formatter import render_email
from src.summarize import summarize_articles


def main(send: bool = True) -> str:
    settings = get_settings()
    articles = dedupe_articles(fetch_articles(settings.feed_urls, settings.max_items))
    digest = summarize_articles(articles, settings)
    html = render_email(digest, articles, ROOT_DIR / "templates" / "email_template.html")

    if send:
        send_email(f"Research Digest - {date.today().isoformat()}", html, settings)

    return digest
