import json
import logging
import threading

from redis import Redis

from app.core.config import REDIS_URL
from app.services.user_client import get_user_details
from app.services.email import send_email

logger = logging.getLogger(__name__)

PAYMENT_EVENTS_CHANNEL = "payments.events"
redis_client = Redis.from_url(REDIS_URL, decode_responses=True)


def _handle_payment_succeeded(event: dict) -> None:
    user_id = event.get("user_id")
    admission_id = event.get("admission_id")
    amount = event.get("amount")
    currency = event.get("currency", "CAD")

    user = get_user_details(user_id)
    email = user["email"]
    if not email:
        logger.warning("Impossible de trouver l'email pour user_id=%s", user_id)
        return

    subject = "Votre paiement d'admission a été reçu"
    html_body = f"""
    <h1>Paiement reçu ✅</h1>
    <p>Bonjour, {user["prenom"]} {user["nom"]}</p>
    <p>Nous avons bien reçu votre paiement pour l'admission #{admission_id}.</p>
    <p>Montant : <b>{amount} {currency.upper()}</b></p>
    <p>Merci de votre confiance.</p>
    """
    send_email(email, subject, html_body)


def _handle_payment_failed(event: dict) -> None:
    user_id = event.get("user_id")
    admission_id = event.get("admission_id")
    amount = event.get("amount")
    currency = event.get("currency", "CAD")

    user = get_user_details(user_id)
    email = user["email"]
    if not email:
        logger.warning("Impossible de trouver l'email pour user_id=%s", user_id)
        return

    subject = "Échec de votre paiement d'admission"
    html_body = f"""
    <h1>Paiement échoué ❌</h1>
    <p>Bonjour, {user["prenom"]} {user["nom"]}</p>
    <p>Votre tentative de paiement pour l'admission #{admission_id} a échoué.</p>
    <p>Montant : <b>{amount} {currency.upper()}</b></p>
    <p>Merci de réessayer ou de contacter le support.</p>
    """
    send_email(email, subject, html_body)


def _listen_loop() -> None:
    logger.info("Notification service: abonnement à Redis channel %s", PAYMENT_EVENTS_CHANNEL)
    pubsub = redis_client.pubsub()
    pubsub.subscribe(PAYMENT_EVENTS_CHANNEL)
    logger.info("Notification service: en attente de messages...")

    for message in pubsub.listen():
        if message["type"] != "message":
            continue

        try:
            data = json.loads(message["data"])
        except Exception:
            logger.exception("Event Redis invalide: %s", message)
            continue

        event_type = data.get("type")
        if event_type == "payment.succeeded":
            _handle_payment_succeeded(data)
        elif event_type == "payment.failed":
            _handle_payment_failed(data)


def start_payment_events_listener() -> None:
    t = threading.Thread(target=_listen_loop, daemon=True)
    t.start()
    logger.info("Notification service: listener Redis démarré.")
