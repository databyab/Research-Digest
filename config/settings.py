from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


ROOT_DIR = Path(__file__).resolve().parents[1]
load_dotenv(ROOT_DIR / ".env")


@dataclass(frozen=True)
class Settings:
    groq_api_key: str
    groq_model: str
    email: str
    app_password: str
    feed_urls: tuple[str, ...]
    max_items: int
    request_timeout: int


def _csv_env(name: str, default: str) -> tuple[str, ...]:
    value = os.getenv(name, default)
    return tuple(item.strip() for item in value.split(",") if item.strip())


def get_settings() -> Settings:
    return Settings(
        groq_api_key=os.getenv("GROQ_API_KEY", "").strip(),
        groq_model=os.getenv("GROQ_MODEL", "llama-3.1-8b-instant").strip(),
        email=os.getenv("EMAIL", "").strip(),
        app_password=os.getenv("APP_PASSWORD", "").strip(),
        feed_urls=_csv_env(
            "FEED_URLS",
            "https://export.arxiv.org/rss/cs.AI,https://export.arxiv.org/rss/cs.CL",
        ),
        max_items=int(os.getenv("MAX_ITEMS", "5")),
        request_timeout=int(os.getenv("REQUEST_TIMEOUT", "45")),
    )