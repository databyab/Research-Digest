from __future__ import annotations

from datetime import date
from html import escape
from pathlib import Path
import re
from urllib.parse import urlparse

from src.fetch import Article


def _safe_url(url: str) -> str:
    parsed = urlparse(url.strip())
    if parsed.scheme not in {"http", "https"}:
        return "#"
    return escape(url.strip(), quote=True)


def _format_inline(text: str) -> str:
    escaped = escape(text.strip())
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)
    return escaped


def render_digest_html(digest: str) -> str:
    blocks: list[str] = []
    list_items: list[str] = []

    def flush_list() -> None:
        if list_items:
            blocks.append(
                '<ul style="margin: 8px 0 16px 22px; padding: 0;">'
                + "".join(list_items)
                + "</ul>"
            )
            list_items.clear()

    for raw_line in digest.splitlines():
        line = raw_line.strip()
        if not line:
            flush_list()
            continue

        if line.startswith(("- ", "* ", "• ")):
            list_items.append(
                f'<li style="margin: 0 0 8px 0;">{_format_inline(line[2:])}</li>'
            )
            continue

        flush_list()

        if line.startswith("### "):
            blocks.append(
                f'<h3 style="font-size: 16px; margin: 22px 0 8px; color: #111827;">{_format_inline(line[4:])}</h3>'
            )
        elif line.startswith("## "):
            blocks.append(
                f'<h2 style="font-size: 18px; margin: 24px 0 10px; color: #111827;">{_format_inline(line[3:])}</h2>'
            )
        elif line.startswith("# "):
            blocks.append(
                f'<h2 style="font-size: 18px; margin: 24px 0 10px; color: #111827;">{_format_inline(line[2:])}</h2>'
            )
        elif line.lower().startswith("link: http"):
            url = line.split(":", 1)[1].strip()
            blocks.append(
                f'<p style="margin: 4px 0 16px;"><a href="{_safe_url(url)}" style="color: #2563eb;">Read source</a></p>'
            )
        elif line.lower().startswith("published:") or line.lower().startswith("reason:"):
            blocks.append(
                f'<p style="margin: 2px 0 8px; color: #667085; font-size: 13px;">{_format_inline(line)}</p>'
            )
        else:
            blocks.append(
                f'<p style="margin: 0 0 14px; color: #344054;">{_format_inline(line)}</p>'
            )

    flush_list()
    return "\n".join(blocks)


def render_email(digest: str, articles: list[Article], template_path: Path) -> str:
    template = template_path.read_text(encoding="utf-8")
    article_links = "\n".join(
        (
            '<li style="margin: 0 0 8px 0;">'
            f'<a href="{_safe_url(article.link)}" style="color: #2563eb;">{escape(article.title)}</a>'
            "</li>"
        )
        for article in articles
    )

    return template.format(
        date=date.today().strftime("%B %d, %Y"),
        digest=render_digest_html(digest),
        article_links=article_links,
    )
