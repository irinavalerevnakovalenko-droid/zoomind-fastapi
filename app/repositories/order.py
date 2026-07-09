from typing import Protocol
from decimal import Decimal
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import OrderStatus
from app.models.order import Order, OrderItem
from app.schemas.pagination import Pagination

class AbstractOrderRepository(Protocol):
    async def create(
        self,
        *,
        user_id: int,
        items_data: list[dict],
        total_price: Decimal,
        ) -> Order:
        ...
        
    async def get_by_id(
        self,
        order_id: int, 
        user_id: int,
        ) -> Order | None:
        ...
        
    async def list_for_user(
        self,
        user_id: int, 
        pagination: Pagination,
        ) -> list[Order]:
        ...
        
    async def update_status(
        self,
        order: Order,
        status: OrderStatus,
    ) -> Order:
        ...
        
    async def list_orders_for_reminder(
        self,
        reminder_before: datetime,
    ) -> list[Order]:
        ...
        
    async def mark_reminder_sent(
        self,
        order: Order,
        sent_at: datetime,
    ) -> Order:
        ...
        

class SQLAlchemyOrderRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def create(
        self,
        *,
        user_id: int,
        items_data: list[dict],
        total_price: Decimal,
        ) -> Order:
        order = Order(
            user_id=user_id,
            total_price=total_price,
        )
        order_items = []
        
        for item_data in items_data:
            order_item = OrderItem(
                product_id=item_data['product_id'],
                quantity=item_data['quantity'],
                unit_price=item_data['unit_price'],
            )
            order_items.append(order_item)
        order.items = order_items
        
        self.session.add(order)
        await self.session.commit()
        await self.session.refresh(order)
        
        return order
    
    async def get_by_id(
        self,
        order_id: int, 
        user_id: int,
        ) -> Order | None:
        
        result = await self.session.execute(
            select(Order).where(
                Order.id == order_id,
                Order.user_id == user_id,    
            )
        )
        return result.scalar_one_or_none()
    
    async def list_for_user(
        self,
        user_id: int, 
        pagination: Pagination,
        ) -> list[Order]:
        query = select(Order).where(
            Order.user_id == user_id,
        )

        query = query.limit(pagination.page_size).offset(pagination.offset)

        result = await self.session.execute(query)
        return list(result.scalars().all())
        
    async def update_status(
        self,
        order: Order,
        status: OrderStatus,
    ) -> Order:
        order.status = status
        
        await self.session.commit()
        await self.session.refresh(order)
        
        return order
    
    async def list_orders_for_reminder(
        self,
        reminder_before: datetime,
    ) -> list[Order]:
        result = await self.session.execute(
            select(Order).where(
                Order.status == OrderStatus.delivered,
                Order.delivered_at <= reminder_before,
                Order.reminder_sent_at.is_(None),
            )
        )
        
        return list(result.scalars().all())
    
    async def mark_reminder_sent(
        self,
        order: Order,
        sent_at: datetime,
    ) -> Order:
        order.reminder_sent_at = sent_at
        
        await self.session.commit()
        await self.session.refresh(order)
        
        return order
    