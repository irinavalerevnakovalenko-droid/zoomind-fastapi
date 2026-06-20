from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import PetSpecies

class Pet(Base):
    __tablename__ = 'pets'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey('users.id'), index=True)
    name: Mapped[str] = mapped_column(String(100), index=True)
    species: Mapped[PetSpecies] = mapped_column(SAEnum(PetSpecies))
    breed: Mapped[str] = mapped_column(String(50))
    age: Mapped[int]
    weight: Mapped[Decimal] = mapped_column(Numeric(5, 2))
    owner: Mapped['User'] = relationship(
        back_populates='pets', 
        lazy='selectin',
    )
    
    
    
    