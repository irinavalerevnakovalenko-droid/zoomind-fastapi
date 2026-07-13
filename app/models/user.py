from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship


from app.core.database import Base
from app.models.order import Order

class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    username: Mapped[str] = mapped_column(String(150), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(default=True)
    is_admin: Mapped[bool] = mapped_column(default=False)
    phone: Mapped[str] = mapped_column(String(30), nullable=False)
    delivery_address: Mapped[str] = mapped_column(String(255), default='')
    is_newsletter_enabled: Mapped[bool] = mapped_column(default=False)
    pets: Mapped[list['Pet']] = relationship(
        back_populates='owner',
        cascade='all, delete-orphan',
        lazy='selectin',
    )
    orders: Mapped[list['Order']] = relationship(
        back_populates='user',
        lazy='selectin',
    )
    

    
        