# app/routers/payments.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from .. import schemas
from ..security.auth import get_current_user, oauth2_scheme
from ..services.payments import create_payment_and_session

router = APIRouter(prefix="/payments", tags=["payments"])


@router.post("/checkout-session")
def create_checkout_session_endpoint(
    payment_in: schemas.PaymentCreate,
    current_user: dict = Depends(get_current_user),
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    payment, session = create_payment_and_session(
        db=db,
        user_payload=current_user,
        token=token,
        payment_in=payment_in,
    )
    return {
        "payment_id": payment.id,
        "checkout_url": session.url,
        "status": payment.status,
    }
