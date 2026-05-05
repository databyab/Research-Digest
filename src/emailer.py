from __future__ import annotations

import smtplib
from email.message import EmailMessage

from config.settings import Settings


def send_email(subject: str, html_body: str, settings: Settings) -> None:
    if not settings.email or not settings.app_password:
        raise RuntimeError("Missing EMAIL or APP_PASSWORD in .env.")

    message = EmailMessage()
    message["From"] = settings.email
    message["To"] = settings.email
    message["Subject"] = subject
    message.set_content("Your email client does not support HTML.")
    message.add_alternative(html_body, subtype="html")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(settings.email, settings.app_password)
        smtp.send_message(message)
