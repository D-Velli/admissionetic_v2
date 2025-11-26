# app/models.py
from sqlalchemy import Column, Integer, String, Numeric, DateTime, Enum as SAEnum, ForeignKey
from sqlalchemy.sql import func
from enum import Enum

from .database import Base

class PaymentStatus(str, Enum):
    PENDING = "PENDING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)      # id venant de user_service
    admission_id = Column(Integer, nullable=False)  # ou programme / autre
    amount = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(10), default="cad")

    status = Column(
        SAEnum(PaymentStatus, name="payment_status_enum"),
        default=PaymentStatus.PENDING,
        nullable=False,
    )

    stripe_payment_intent_id = Column(String(255), unique=True, nullable=True)
    stripe_checkout_session_id = Column(String(255), unique=True, nullable=True)

    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        default=func.now(),
        onupdate=func.now(),
    )
