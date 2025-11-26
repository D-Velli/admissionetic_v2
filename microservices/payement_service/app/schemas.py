from decimal import Decimal
from enum import Enum
from pydantic import BaseModel

class PaymentStatus(str, Enum):
    PENDING = "PENDING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    CANCELED = "CANCELED"

class PaymentCreate(BaseModel):
    admission_id: int
    

class PaymentPublic(BaseModel):
    id: int
    user_id: int
    admission_id: int | None
    amount: Decimal
    currency: str
    status: PaymentStatus

    class Config:
        from_attributes = True  # pydantic v2
