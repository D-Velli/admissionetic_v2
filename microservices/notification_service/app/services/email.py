import smtplib
from email.message import EmailMessage
import logging

from app.core.config import SMTP_HOST, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD, EMAIL_FROM, BASE_DIR
from jinja2 import Environment, FileSystemLoader, select_autoescape

logger = logging.getLogger(__name__)

env = Environment(
    loader=FileSystemLoader(BASE_DIR / "templates"),
    autoescape=select_autoescape(["html", "xml"]),
)

def render_template(template_name: str, **context) -> str:
    template = env.get_template(template_name)
    return template.render(**context)


def send_email(to_email: str, subject: str, html_body: str, text_body: str | None = None) -> None:
    msg = EmailMessage()
    msg["From"] = EMAIL_FROM
    msg["To"] = to_email
    msg["Subject"] = subject

    if not text_body:
        text_body = "Veuillez utiliser un client compatible HTML."

    msg.set_content(text_body)
    msg.add_alternative(html_body, subtype="html")

    try:
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as smtp:
            if SMTP_USERNAME and SMTP_PASSWORD:
                smtp.login(SMTP_USERNAME, SMTP_PASSWORD)
            smtp.send_message(msg)
        logger.info("Email envoyé à %s", to_email)
    except Exception:
        logger.exception("Erreur lors de l'envoi d'email à %s", to_email)
