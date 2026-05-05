# Research Digest

Research Digest fetches papers from RSS feeds, optionally summarizes them with Groq, renders an HTML digest, and emails it to your own Gmail inbox.

The app is intentionally personal-use focused: it sends from `EMAIL` to the same `EMAIL` address configured in `.env`.

## Features

- Fetches research items from configurable RSS feeds
- Deduplicates repeated entries
- Summarizes articles with Groq chat completions when configured
- Falls back to a plain feed digest when Groq is missing or unavailable
- Generates a clean HTML email
- Sends the digest to yourself through Gmail SMTP

## Requirements

- Python 3.12 or newer
- A Groq API key, optional but recommended for summaries
- A Gmail account with an app password

## Setup

Create and activate a virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Update `.env`:

```env
EMAIL=your_email@gmail.com
APP_PASSWORD=your_gmail_app_password

GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama-3.1-8b-instant

FEED_URLS=https://export.arxiv.org/rss/cs.AI,https://export.arxiv.org/rss/cs.CL
MAX_ITEMS=5
REQUEST_TIMEOUT=45
```

## Project Structure

```text
research-digest/
  config/
    settings.py
  src/
    emailer.py
    fetch.py
    filter.py
    formatter.py
    main.py
    summarize.py
  templates/
    email_template.html
  .env.example
  requirements.txt
  run.py
```

