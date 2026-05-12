from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from decimal import Decimal


class OrderDetailCreate(BaseModel):
    orderNumber: int = Field(..., description="FK → orders.orderNumber (part of composite PK)")
    productCode: str = Field(..., description="FK → products.productCode (part of composite PK)")
    quantityOrdered: int = Field(..., gt=0, description="Quantity ordered — must be > 0")
    priceEach: Decimal = Field(..., gt=0, decimal_places=2, description="Price per unit at time of order")
    orderLineNumber: int = Field(..., ge=1, le=32767, description="Line number within order (smallint: 1–32767)")


class OrderDetailUpdate(BaseModel):
    quantityOrdered: Optional[int] = Field(None, gt=0, description="Quantity ordered — must be > 0")
    priceEach: Optional[Decimal] = Field(None, gt=0, decimal_places=2, description="Price per unit")
    orderLineNumber: Optional[int] = Field(None, ge=1, le=32767, description="Line number within order")


class OrderDetailOut(OrderDetailCreate):
    model_config = ConfigDict(from_attributes=True)