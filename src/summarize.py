from __future__ import annotations

import requests

from config.settings import Settings
from src.fetch import Article


GROQ_CHAT_COMPLETIONS_URL = "https://api.groq.com/openai/v1/chat/completions"


def build_plain_digest(articles: list[Article], reason: str | None = None) -> str:
    if not articles:
        return "No new articles found."

    intro = "## Research Items"
    note = "Groq summarization was skipped. Sending the fetched research items instead."
    if reason:
        note = f"{note}\nReason: {reason}"

    items = []
    for article in articles:
        summary = article.summary.replace("\n", " ").strip()
        if len(summary) > 700:
            summary = f"{summary[:697]}..."
        items.append(
            "\n".join(
                [
                    f"### {article.title}",
                    f"Published: {article.published}",
                    f"Link: {article.link}",
                    summary,
                ]
            )
        )

    return f"{intro}\n\n{note}\n\n" + "\n\n".join(items)


def summarize_articles(articles: list[Article], settings: Settings) -> str:
    if not settings.groq_api_key:
        return build_plain_digest(articles, "GROQ_API_KEY is not configured.")

    if not articles:
        return "No new articles found."

    article_text = "\n\n".join(
        f"Title: {article.title}\nPublished: {article.published}\nLink: {article.link}\nAbstract: {article.summary}"
        for article in articles
    )
    payload = {
        "model": settings.groq_model,
        "temperature": 0.2,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You write concise research digests in clean Markdown. Use '## Top Takeaways' first, "
                    "then 3-5 bullets. After that, use '## Papers' and one '### Title' section per item. "
                    "Each item should have 2-3 bullets and a short 'Why it matters:' sentence. "
                    "Do not use tables."
                ),
            },
            {"role": "user", "content": f"Create today's research digest from these items:\n\n{article_text}"},
        ],
    }

    try:
        response = requests.post(
            GROQ_CHAT_COMPLETIONS_URL,
            headers={
                "Authorization": f"Bearer {settings.groq_api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=settings.request_timeout,
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()
    except requests.RequestException as exc:
        return build_plain_digest(articles, f"Groq request failed: {exc}")
    except (KeyError, IndexError, TypeError) as exc:
        return build_plain_digest(articles, f"Groq returned an unexpected response: {exc}")
