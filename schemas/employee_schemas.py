from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import Optional, List


class EmployeeCreate(BaseModel):
    employeeNumber: int = Field(..., description="Unique employee number — provided by client")
    lastName: str = Field(..., max_length=50, description="Employee last name")
    firstName: str = Field(..., max_length=50, description="Employee first name")
    extension: str = Field(..., max_length=10, description="Phone extension e.g. 'x5800'")
    email: EmailStr = Field(..., description="Must be a valid email address")
    officeCode: str = Field(..., max_length=10, description="Foreign key to offices.officeCode")
    reportsTo: Optional[int] = Field(None, description="FK to employees.employeeNumber — null for top manager")
    jobTitle: str = Field(..., max_length=50, description="Job title e.g. 'Sales Rep', 'VP Sales'")


class EmployeeUpdate(BaseModel):
    lastName: Optional[str] = Field(None, max_length=50)
    firstName: Optional[str] = Field(None, max_length=50)
    extension: Optional[str] = Field(None, max_length=10)
    email: Optional[EmailStr] = None
    officeCode: Optional[str] = Field(None, max_length=10)
    reportsTo: Optional[int] = None
    jobTitle: Optional[str] = Field(None, max_length=50)


class CustomerOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    customerNumber: int
    customerName: str
    contactLastName: str
    contactFirstName: str
    phone: str
    city: str
    country: str
    creditLimit: Optional[float] = None


class EmployeeOut(EmployeeCreate):
    model_config = ConfigDict(from_attributes=True)

    customers: List[CustomerOut] = Field(default=[], description="Customers managed by this employee")