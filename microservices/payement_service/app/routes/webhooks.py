import json
import logging
from datetime import datetime, timezone

from fastapi import APIRouter, Request, Header, HTTPException, Depends
from redis import Redis
from sqlalchemy.orm import Session

from ..database import get_db
from ..config import STRIPE_WEBHOOK_SECRET, REDIS_URL
from ..models import Payment, PaymentStatus
from ..services.stripe_client import retrieve_event

router = APIRouter(prefix="/webhooks", tags=["webhooks"])
logger = logging.getLogger(__name__)
PAYMENT_EVENTS_CHANNEL = "payments.events"
redis_client = Redis.from_url(REDIS_URL, decode_responses=True)


def emit_payment_succeeded_event(payment: Payment) -> None:
    payload = {
        "type": "payment.succeeded",
        "payment_id": payment.id,
        "user_id": payment.user_id,
        "admission_id": payment.admission_id,
        "amount": str(payment.amount),
        "currency": payment.currency,
        "status": payment.status.value if isinstance(payment.status, PaymentStatus) else payment.status,
        "stripe_payment_intent_id": payment.stripe_payment_intent_id,
        "stripe_checkout_session_id": payment.stripe_checkout_session_id,
        "published_at": datetime.now(timezone.utc).isoformat(),
    }

    try:
        redis_client.publish(PAYMENT_EVENTS_CHANNEL, json.dumps(payload))
    except Exception:
        logger.exception("Failed to publish Redis payment event")

def emit_payment_failed_event(payment: Payment) -> None:
    payload = {
        "type": "payment.failed",
        "payment_id": payment.id,
        "user_id": payment.user_id,
        "admission_id": payment.admission_id,
        "amount": str(payment.amount),
        "currency": payment.currency,
        "status": payment.status.value,
        "stripe_payment_intent_id": payment.stripe_payment_intent_id,
        "stripe_checkout_session_id": payment.stripe_checkout_session_id,
        "published_at": datetime.now(timezone.utc).isoformat(),
    }
    try:
        redis_client.publish(PAYMENT_EVENTS_CHANNEL, json.dumps(payload))
    except Exception:
        logger.exception("Failed to publish Redis payment.failed event")


@router.post("/stripe")
async def stripe_webhook(
    request: Request,
    stripe_signature: str = Header(None, alias="Stripe-Signature"),
    db: Session = Depends(get_db),
):
    payload = await request.body()

    try:
        event = retrieve_event(payload, stripe_signature, STRIPE_WEBHOOK_SECRET)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid signature")

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        payment_id = session["metadata"].get("payment_id")

        payment: Payment | None = db.query(Payment).get(int(payment_id))
        if payment:
            payment.status = PaymentStatus.SUCCEEDED
            db.commit()
            emit_payment_succeeded_event(payment)

    # JE VAIS GERER CECI PLUS TARD QUAND UN PAIEMENT EST ANNULE
    
    # elif event["type"] == "payment_intent.payment_failed":
    #     intent = event["data"]["object"]
    #     intent_id = intent["id"]

    #     payment: Payment | None = (
    #         db.query(Payment)
    #         .filter(Payment.stripe_payment_intent_id == intent_id)
    #         .first()
    #     )
    #     if payment and payment.status == PaymentStatus.PENDING:
    #         payment.status = PaymentStatus.FAILED
    #         db.commit()
    #         emit_payment_failed_event(payment)

    return {"received": True}
