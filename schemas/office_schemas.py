from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional, List
import re


class OfficeCreate(BaseModel):
    officeCode: str = Field(..., max_length=10, description="Primary key — short office code e.g. '1', '7'")
    city: str = Field(..., max_length=50, description="City name")
    phone: str = Field(..., max_length=50, description="Phone number including country code")
    addressLine1: str = Field(..., max_length=50, description="Main address line")
    addressLine2: Optional[str] = Field(None, max_length=50, description="Optional second address line")
    state: Optional[str] = Field(None, max_length=50, description="State or region — nullable")
    country: str = Field(..., max_length=50, description="Country name")
    postalCode: str = Field(..., max_length=15, description="Postal or ZIP code")
    territory: str = Field(..., max_length=10, description="Sales territory e.g. 'NA', 'EMEA', 'APAC'")

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v):
        cleaned = re.sub(r'[\s\+\-\(\)]', '', v)
        if not cleaned.isdigit():
            raise ValueError('Phone number must contain only digits, spaces, +, -, or parentheses')
        if len(cleaned) < 7:
            raise ValueError('Phone number must have at least 7 digits')
        return v


class OfficeUpdate(BaseModel):
    city: Optional[str] = Field(None, max_length=50)
    phone: Optional[str] = Field(None, max_length=50)
    addressLine1: Optional[str] = Field(None, max_length=50)
    addressLine2: Optional[str] = Field(None, max_length=50)
    state: Optional[str] = Field(None, max_length=50)
    country: Optional[str] = Field(None, max_length=50)
    postalCode: Optional[str] = Field(None, max_length=15)
    territory: Optional[str] = Field(None, max_length=10)

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


class EmployeeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    employeeNumber: int
    lastName: str
    firstName: str
    extension: str
    email: str
    officeCode: str
    reportsTo: Optional[int] = None
    jobTitle: str


class OfficeOut(OfficeCreate):
    model_config = ConfigDict(from_attributes=True)

    employees: List[EmployeeOut] = Field(default=[], description="Employees working at this office")