from datetime import datetime
from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, Field, ConfigDict

from app.models.enums import OrderStatus

Quantity = Annotated[int, Field(ge=1)]


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: Quantity
    
OrderItems = Annotated[list[OrderItemCreate], Field(min_length=1)]
    
class OrderCreate(BaseModel):
    items: OrderItems
    
class OrderItemRead(BaseModel):
    id: int
    product_id: int
    quantity: int
    unit_price: Decimal

    model_config = ConfigDict(from_attributes=True)
    
class OrderRead(BaseModel):
    id: int
    user_id: int
    status: OrderStatus
    items: list[OrderItemRead]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class OrderStatusUpdate(BaseModel):
    status: OrderStatus
    
