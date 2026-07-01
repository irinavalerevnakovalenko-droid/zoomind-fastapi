from decimal import Decimal

from sqlalchemy import Enum as SAEnum
from sqlalchemy import Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.enums import ProductCategory, ProductSpecies

class Product(Base):
    __tablename__ = 'products'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    sku: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(150), index=True)
    category: Mapped[ProductCategory] = mapped_column(SAEnum(ProductCategory))
    species: Mapped[ProductSpecies] = mapped_column(SAEnum(ProductSpecies))
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    stock: Mapped[int] = mapped_column(default=0)
    description: Mapped[str] = mapped_column(Text, default='')
    weight_kg: Mapped[Decimal | None] = mapped_column(Numeric(6, 2), nullable=True)
