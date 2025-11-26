import json
import logging
import threading

from redis import Redis

from app.core.config import REDIS_URL
from app.database import SessionLocal
from app.models import Admission, StatutAdmissionEnum

logger = logging.getLogger(__name__)

PAYMENT_EVENTS_CHANNEL = "payments.events"
redis_client = Redis.from_url(REDIS_URL, decode_responses=True)


def _handle_payment_succeeded(event: dict) -> None:
    admission_id = event.get("admission_id")
    user_id = event.get("user_id")

    if not admission_id:
        logger.warning("payment.succeeded event without admission_id: %s", event)
        return

    db = SessionLocal()
    try:
        adm = db.query(Admission).filter(Admission.id == admission_id).first()
        if not adm:
            logger.warning("Admission %s not found, ignoring payment event", admission_id)
            return

        # (optionnel) sécurité : vérifier que le paiement vient bien du bon user
        if user_id is not None and adm.user_id != int(user_id):
            logger.warning(
                "User mismatch for admission %s: adm.user_id=%s, event.user_id=%s",
                admission_id, adm.user_id, user_id
            )
            return

        # idempotent : si c'est déjà accepté, on ne refait rien
        if adm.status == StatutAdmissionEnum.ACCEPTEE:
            logger.info("Admission %s already ACCEPTEE, skipping", admission_id)
            return

        adm.status = StatutAdmissionEnum.ACCEPTEE
        db.commit()
        logger.info("Admission %s marked as ACCEPTEE from payment event", admission_id)
    except Exception:
        logger.exception("Error while handling payment.succeeded event")
        db.rollback()
    finally:
        db.close()


def _listen_loop() -> None:
    pubsub = redis_client.pubsub()
    pubsub.subscribe(PAYMENT_EVENTS_CHANNEL)
    logger.info("Subscribed to Redis channel %s", PAYMENT_EVENTS_CHANNEL)
    logger.info("Redis listener: subscribed and waiting for messages...")


    for message in pubsub.listen():
        if message["type"] != "message":
            continue

        try:
            data = json.loads(message["data"])
        except Exception:
            logger.exception("Invalid JSON in Redis payment event: %s", message)
            continue

        if data.get("type") == "payment.succeeded":
            _handle_payment_succeeded(data)


def start_payment_events_listener() -> None:
    logger.info("Starting Redis payment events listener thread...")
    thread = threading.Thread(target=_listen_loop, daemon=True)
    thread.start()
    logger.info("Started payment events listener thread")
