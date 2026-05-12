import smtplib
from email.mime.text import MIMEText

from config.settings import Settings


def send_email(subject: str, html_content: str, settings: Settings) -> None:
    msg = MIMEText(html_content, "html")
    msg["Subject"] = subject
    msg["From"] = settings.email
    msg["To"] = settings.email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(settings.email, settings.app_password)
        server.send_message(msg)