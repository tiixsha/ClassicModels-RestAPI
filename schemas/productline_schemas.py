from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List


class ProductLineCreate(BaseModel):
    productLine: str = Field(..., max_length=50, description="Primary key — category name")
    textDescription: Optional[str] = Field(None, max_length=4000, description="Plain text description")
    htmlDescription: Optional[str] = Field(None, description="HTML version of description")


class ProductLineUpdate(BaseModel):
    textDescription: Optional[str] = Field(None, max_length=4000)
    htmlDescription: Optional[str] = None


class ProductOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    productCode: str
    productName: str
    productLine: str
    productScale: str
    productVendor: str
    productDescription: str
    quantityInStock: int
    buyPrice: float
    MSRP: float


class ProductLineOut(ProductLineCreate):
    model_config = ConfigDict(from_attributes=True)

    # image excluded from output — binary data not safe for JSON
    products: List[ProductOut] = Field(default=[], description="Products in this product line")