from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional
from datetime import date
from decimal import Decimal
import datetime


class PaymentCreate(BaseModel):
    customerNumber: int = Field(..., description="FK → customers.customerNumber (part of composite PK)")
    checkNumber: str = Field(..., max_length=50, description="Unique check identifier (part of composite PK)")
    paymentDate: date = Field(..., description="Date the payment was made. Format: YYYY-MM-DD")
    amount: Decimal = Field(..., gt=0, decimal_places=2, description="Payment amount — must be > 0")

    @field_validator("paymentDate")
    @classmethod
    def payment_date_must_not_be_future(cls, v):
        if v > datetime.date.today():
            raise ValueError("paymentDate cannot be in the future")
        return v


class PaymentUpdate(BaseModel):
    paymentDate: Optional[date] = None
    amount: Optional[Decimal] = Field(None, gt=0, decimal_places=2, description="Payment amount — must be > 0")

    @field_validator("paymentDate")
    @classmethod
    def payment_date_must_not_be_future(cls, v):
        if v is not None and v > datetime.date.today():
            raise ValueError("paymentDate cannot be in the future")
        return v


class PaymentOut(PaymentCreate):
    model_config = ConfigDict(from_attributes=True)