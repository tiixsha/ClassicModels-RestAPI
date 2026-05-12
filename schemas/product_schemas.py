from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional, List
from decimal import Decimal


class ProductCreate(BaseModel):
    productCode: str = Field(..., max_length=15, description="Unique product code e.g. 'S10_1678'")
    productName: str = Field(..., max_length=70, description="Full product name")
    productLine: str = Field(..., max_length=50, description="Foreign key to productlines")
    productScale: str = Field(..., max_length=10, description="Scale of the model e.g. '1:10'")
    productVendor: str = Field(..., max_length=50, description="Vendor name")
    productDescription: str = Field(..., description="Full text description")
    quantityInStock: int = Field(..., ge=0, description="Stock quantity must be >= 0")
    buyPrice: Decimal = Field(..., gt=0, decimal_places=2, description="Cost price")
    MSRP: Decimal = Field(..., gt=0, decimal_places=2, description="Retail price")

    @field_validator('MSRP')
    @classmethod
    def msrp_must_be_gte_buyprice(cls, v, values):
        if 'buyPrice' in values.data and v < values.data['buyPrice']:
            raise ValueError('MSRP must be greater than or equal to buyPrice')
        return v


class ProductUpdate(BaseModel):
    productName: Optional[str] = Field(None, max_length=70)
    productLine: Optional[str] = Field(None, max_length=50)
    productScale: Optional[str] = Field(None, max_length=10)
    productVendor: Optional[str] = Field(None, max_length=50)
    productDescription: Optional[str] = None
    quantityInStock: Optional[int] = Field(None, ge=0)
    buyPrice: Optional[Decimal] = Field(None, gt=0, decimal_places=2)
    MSRP: Optional[Decimal] = Field(None, gt=0, decimal_places=2)


class OrderDetailOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    orderNumber: int
    productCode: str
    quantityOrdered: int
    priceEach: float
    orderLineNumber: int


class ProductOut(ProductCreate):
    model_config = ConfigDict(from_attributes=True)

    buyPrice: float
    MSRP: float
    orderdetails: List[OrderDetailOut] = Field(default=[], description="Order details for this product")