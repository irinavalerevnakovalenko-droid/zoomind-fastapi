from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import ProductCategory, ProductSpecies

ProductSku = Annotated[str, Field(min_length=2, max_length=50)]
ProductName = Annotated[str, Field(min_length=2, max_length=150)]
ProductPrice = Annotated[Decimal, Field(gt=0, max_digits=10, decimal_places=2)]
ProductStock = Annotated[int, Field(ge=0)]
ProductDescription = Annotated[str, Field(max_length=200)]
ProductWeight = Annotated[Decimal, Field(gt=0, max_digits=6, decimal_places=2)]

class ProductBase(BaseModel):
    sku: ProductSku
    name: ProductName
    category: ProductCategory
    species: ProductSpecies
    price: ProductPrice
    stock: ProductStock
    description: ProductDescription = ''
    weight_kg: ProductWeight | None = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    sku: ProductSku | None = None
    name: ProductName | None = None
    category: ProductCategory | None = None
    species: ProductSpecies | None = None
    price: ProductPrice | None = None
    stock: ProductStock | None = None
    description: ProductDescription | None = None
    weight_kg: ProductWeight | None = None
    
class ProductRead(ProductBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
    
    
class ProductFilter(BaseModel):
    category: ProductCategory | None = None
    species: ProductSpecies | None = None
    name_contains: str | None = None
    min_price: ProductPrice | None = None
    max_price: ProductPrice | None = None
    in_stock: bool | None = None
