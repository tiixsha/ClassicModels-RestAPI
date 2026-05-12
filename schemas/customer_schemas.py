from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional, List
from datetime import date
import re


class OrderOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    orderNumber: int
    orderDate: date
    requiredDate: date
    shippedDate: Optional[date] = None
    status: str = Field(..., max_length=15, description="Current status of the order")
    comments: Optional[str] = Field(None, description="Additional comments about the order")
    customerNumber: int


class PaymentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    customerNumber: int
    checkNumber: str = Field(..., max_length=50, description="Unique check number for the payment")
    paymentDate: date
    amount: float = Field(..., gt=0, description="Payment amount must be greater than 0")


class CustomerCreate(BaseModel):
    customerNumber: int = Field(..., description="Unique customer number — must be provided manually")
    customerName: str = Field(..., min_length=1, max_length=50, description="Full name of the customer")
    contactLastName: str = Field(..., min_length=1, max_length=50, description="Last name of contact person")
    contactFirstName: str = Field(..., min_length=1, max_length=50, description="First name of contact person")
    phone: str = Field(..., min_length=7, max_length=50, description="Customer phone number")
    addressLine1: str = Field(..., min_length=1, max_length=50, description="Primary address line")
    addressLine2: Optional[str] = Field(None, max_length=50, description="Secondary address line")
    city: str = Field(..., min_length=1, max_length=50, description="City of the customer")
    state: Optional[str] = Field(None, max_length=50, description="State of the customer")
    postalCode: Optional[str] = Field(None, max_length=15, description="Postal code of the customer")
    country: str = Field(..., min_length=1, max_length=50, description="Country of the customer")
    salesRepEmployeeNumber: Optional[int] = Field(None, description="Employee number of the sales representative")
    creditLimit: Optional[float] = Field(None, ge=0, description="Credit limit must be zero or positive")

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v):
        cleaned = re.sub(r'[\s\+\-\(\)]', '', v)
        if not cleaned.isdigit():
            raise ValueError('Phone number must contain only digits, spaces, +, -, or parentheses')
        if len(cleaned) < 7:
            raise ValueError('Phone number must have at least 7 digits')
        return v


class CustomerUpdate(BaseModel):
    customerName: Optional[str] = Field(None, min_length=1, max_length=50, description="Full name of the customer")
    contactLastName: Optional[str] = Field(None, min_length=1, max_length=50, description="Last name of contact person")
    contactFirstName: Optional[str] = Field(None, min_length=1, max_length=50, description="First name of contact person")
    phone: Optional[str] = Field(None, min_length=7, max_length=50, description="Customer phone number")
    addressLine1: Optional[str] = Field(None, min_length=1, max_length=50, description="Primary address line")
    addressLine2: Optional[str] = Field(None, max_length=50, description="Secondary address line")
    city: Optional[str] = Field(None, min_length=1, max_length=50, description="City of the customer")
    state: Optional[str] = Field(None, max_length=50, description="State of the customer")
    postalCode: Optional[str] = Field(None, max_length=15, description="Postal code of the customer")
    country: Optional[str] = Field(None, min_length=1, max_length=50, description="Country of the customer")
    salesRepEmployeeNumber: Optional[int] = Field(None, description="Employee number of the sales representative")
    creditLimit: Optional[float] = Field(None, ge=0, description="Credit limit must be zero or positive")

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v):
        if v is None:
            return v
        cleaned = re.sub(r'[\s\+\-\(\)]', '', v)
        if not cleaned.isdigit():
            raise ValueError('Phone number must contain only digits, spaces, +, -, or parentheses')
        if len(cleaned) < 7:
            raise ValueError('Phone number must have at least 7 digits')
        return v


class CustomerOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    customerNumber: int
    customerName: str = Field(..., description="Full name of the customer")
    contactLastName: str = Field(..., description="Last name of contact person")
    contactFirstName: str = Field(..., description="First name of contact person")
    phone: str = Field(..., description="Customer phone number")
    addressLine1: str = Field(..., description="Primary address line")
    addressLine2: Optional[str] = Field(None, description="Secondary address line")
    city: str = Field(..., description="City of the customer")
    state: Optional[str] = Field(None, description="State of the customer")
    postalCode: Optional[str] = Field(None, description="Postal code of the customer")
    country: str = Field(..., description="Country of the customer")
    salesRepEmployeeNumber: Optional[int] = Field(None, description="Employee number of the sales representative")
    creditLimit: Optional[float] = Field(None, description="Credit limit of the customer")
    orders: List[OrderOut] = Field(default=[], description="List of orders placed by the customer")
    payments: List[PaymentOut] = Field(default=[], description="List of payments made by the customer")