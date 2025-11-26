import stripe
from ..config import STRIPE_SECRET_KEY

stripe.api_key = STRIPE_SECRET_KEY

def create_checkout_session(amount: int, currency: str, metadata: dict) -> stripe.checkout.Session:
    return stripe.checkout.Session.create(
        mode="payment",
        line_items=[
            {
                "price_data": {
                    "currency": currency,
                    "product_data": {"name": "Frais d'admission"},
                    "unit_amount": amount,  # en cents
                },
                "quantity": 1,
            }
        ],
        metadata=metadata,
        success_url="http://127.0.0.1:3000/success?session_id={CHECKOUT_SESSION_ID}",
        cancel_url="http://127.0.0.1:3000/cancel",
    )

def retrieve_event(payload: bytes, sig_header: str, webhook_secret: str):
    return stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
