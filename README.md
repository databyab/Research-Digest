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
- Supports dry runs without sending email

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

Create your environment file:

```powershell
Copy-Item .env.example .env
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

## Usage

Preview the digest without sending email:

```powershell
.\venv\Scripts\python.exe run.py --no-send
```

Generate and send the digest to yourself:

```powershell
.\venv\Scripts\python.exe run.py
```

## Configuration

| Variable | Required | Description |
| --- | --- | --- |
| `EMAIL` | Yes | Gmail address used as both sender and recipient |
| `APP_PASSWORD` | Yes | Gmail app password for SMTP login |
| `GROQ_API_KEY` | No | Groq API key used for summarization. Email still sends without it |
| `GROQ_MODEL` | No | Groq model name. Defaults to `llama-3.1-8b-instant` |
| `FEED_URLS` | No | Comma-separated RSS feed URLs |
| `MAX_ITEMS` | No | Maximum number of feed items to summarize |
| `REQUEST_TIMEOUT` | No | HTTP timeout in seconds |

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

## Troubleshooting

Groq returns `401 Unauthorized`

The Groq key is missing, invalid, expired, or copied with extra spaces. The app will still send a plain digest without AI summarization.

`ModuleNotFoundError: No module named 'feedparser'`

Run the app with the project virtual environment:

```powershell
.\venv\Scripts\python.exe run.py --no-send
```

RSS feeds are blocked or unavailable

If feeds cannot be reached, the app skips them and still completes. Check your internet connection, firewall rules, and `FEED_URLS`.

`Missing EMAIL or APP_PASSWORD in .env`

Set both values in `.env`. Gmail requires an app password, not your normal account password.

## Production Notes

- Keep `.env` private and out of version control.
- Use `--no-send` after changing feeds, models, or templates.
- For scheduled delivery, run `.\venv\Scripts\python.exe run.py` from Windows Task Scheduler.
- The current email behavior is self-only by design.
