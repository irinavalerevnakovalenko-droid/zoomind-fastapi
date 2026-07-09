from decimal import Decimal
from datetime import datetime

from sqlalchemy import ForeignKey, Numeric, DateTime, func
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import OrderStatus

class Order(Base):
    __tablename__ = 'orders'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), index=True)
    status: Mapped[OrderStatus] = mapped_column(
        SAEnum(OrderStatus), 
        default=OrderStatus.pending,
        )
    total_price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        default=0,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
    delivered_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    reminder_sent_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    user: Mapped['User'] = relationship(
        back_populates='orders',
        lazy='selectin',
    )
    items: Mapped[list['OrderItem']] = relationship(
        back_populates='order',
        lazy='selectin',
        cascade='all, delete-orphan',
    )
    
class OrderItem(Base):
    __tablename__ = 'order_items'

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id'), index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'), index=True)
    quantity: Mapped[int] = mapped_column()
    unit_price: Mapped[Decimal] = mapped_column(Numeric(10, 2))

    order: Mapped['Order'] = relationship(
        back_populates='items',
        lazy='selectin',
    )

    product: Mapped['Product'] = relationship(
        lazy='selectin',
    )
    
    
    
    


