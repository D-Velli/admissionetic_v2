from sqlalchemy.orm import Session
from .. import models, schemas
from ..clients.admission_client import get_admission_or_raise
from .stripe_client import create_checkout_session, retrieve_event
from fastapi import HTTPException, status
from ..security.auth import oauth2_scheme
from decimal import Decimal
import json

ALLOWED_ADMISSION_STATUSES = {"en_attente"}

def create_payment_and_session(
    db: Session,
    user_payload: dict,
    token: str,
    payment_in: schemas.PaymentCreate,
):
    user_id = int(user_payload["sub"])
    

    # 1. Vérifier que l'admission existe (appel HTTP au microservice)
    admission = get_admission_or_raise(payment_in.admission_id, token)

    # 2. Vérifier l'appartenance
    if admission.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admission does not belong to current user",
        )
        
     # 3. S'assurer que n'est pas deja payer
    existing_payment = (
        db.query(models.Payment)
        .filter(
            models.Payment.user_id == user_id,
            models.Payment.admission_id == payment_in.admission_id,
            models.Payment.status.in_(
                [models.PaymentStatus.PENDING, models.PaymentStatus.SUCCEEDED]
            ),
        )
        .order_by(models.Payment.created_at.desc())
        .first()
    )
    
    if existing_payment:
        # déjà payé
        if existing_payment.status == models.PaymentStatus.SUCCEEDED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cette admission a déjà été payée.",
            )
        # paiement en cours
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Un paiement est déjà en cours pour cette admission.",
        )

    # 4. Vérifier le status de l'admission
    if admission.status not in ALLOWED_ADMISSION_STATUSES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Admission status '{admission.status}' does not allow payment",
        )

    # 4. Montant & currency depuis admission_service (pas du front)
    amount = Decimal(str(admission.amount))
    currency = admission.currency.lower()

    # 5. Créer l'entrée Payment en DB
    payment = models.Payment(
        user_id=user_id,
        admission_id=admission.id,
        amount=amount,
        currency=currency,
    )
    db.add(payment)
    db.commit()
    db.refresh(payment)

    # 6. Créer la session Stripe
    session = create_checkout_session(
        amount=int(payment.amount * 100),
        currency=payment.currency,
        metadata={
            "payment_id": str(payment.id),
            "user_id": str(user_id),
            "admission_id": str(admission.id),
        },
    )

    payment.stripe_checkout_session_id = session.id
    db.commit()
    db.refresh(payment)
    
    # 7. stocker la variable stripe_payment_intent_id
    

    return payment, session


# def create_payment_and_session(
#     db: Session,
#     user_id: int,
#     payment_in: schemas.PaymentCreate,
# ):
#     # 1. créer l’entrée Payment
#     payment = models.Payment(
#         user_id=user_id,
#         admission_id=payment_in.admission_id,
#         amount=payment_in.amount,
#         currency=payment_in.currency,
#     )
#     db.add(payment)
#     db.commit()
#     db.refresh(payment)

#     # 2. créer la session Stripe (amount en cents)
#     session = create_checkout_session(
#         amount=int(payment.amount * 100),
#         currency=payment.currency,
#         metadata={"payment_id": str(payment.id), "user_id": str(user_id)},
#     )

#     payment.stripe_checkout_session_id = session.id
#     db.commit()
#     db.refresh(payment)

#     return payment, session
