from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional, List
from datetime import date
from decimal import Decimal
from typing import Literal


class OrderCreate(BaseModel):
    orderNumber: int = Field(..., description="Unique order number — provided by client")
    orderDate: date = Field(..., description="Date the order was placed. Format: YYYY-MM-DD")
    requiredDate: date = Field(..., description="Date by which order must be delivered")
    shippedDate: Optional[date] = Field(None, description="Actual ship date — null if not yet shipped")
    status: Literal["Shipped", "Resolved", "Cancelled", "On Hold", "Disputed", "In Process"] = Field(..., description="Order status")
    comments: Optional[str] = Field(None, description="Free-text notes about the order")
    customerNumber: int = Field(..., description="Foreign key to customers.customerNumber")

    @field_validator('requiredDate')
    @classmethod
    def required_date_must_be_after_order_date(cls, v, values):
        if 'orderDate' in values.data and v < values.data['orderDate']:
            raise ValueError('requiredDate must be after orderDate')
        return v


class OrderUpdate(BaseModel):
    orderDate: Optional[date] = None
    requiredDate: Optional[date] = None
    shippedDate: Optional[date] = None
    status: Optional[Literal["Shipped", "Resolved", "Cancelled", "On Hold", "Disputed", "In Process"]] = None
    comments: Optional[str] = None
    customerNumber: Optional[int] = None


class OrderDetailOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    orderNumber: int
    productCode: str
    quantityOrdered: int
    priceEach: float
    orderLineNumber: int


class OrderOut(OrderCreate):
    model_config = ConfigDict(from_attributes=True)

    orderdetails: List[OrderDetailOut] = Field(default=[], description="Line items in this order")