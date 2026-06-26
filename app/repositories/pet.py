from decimal import Decimal
from typing import Protocol

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import PetSpecies
from app.models.pet import Pet
from app.schemas.pet import PetFilter
from app.schemas.pagination import Pagination

class AbstractPetRepository(Protocol):
    async def create(
        self,
        *,
        owner_id: int,
        name: str,
        species: PetSpecies,
        breed: str,
        age: int,
        weight: Decimal,
    ) -> Pet:
        ...
        
    async def get_by_id(self, pet_id: int, owner_id: int) -> Pet | None:
        ...
        
    async def list_for_owner(
        self,
        owner_id: int,
        filters: PetFilter,
        pagination: Pagination,
        ) -> list[Pet]:
        ...
        
    async def update(self, pet: Pet, data: dict) -> Pet:
        ...
        
    async def delete(self, pet: Pet) -> None:
        ... 

class SQLAlchemyPetRepository(AbstractPetRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def create(
        self,
        *,
        owner_id: int,
        name: str,
        species: PetSpecies,
        breed: str,
        age: int,
        weight: Decimal,
    ) -> Pet:
        pet = Pet(
            owner_id=owner_id,
            name=name,
            species=species,
            breed=breed,
            age=age,
            weight=weight,    
        )
        
        self.session.add(pet)
        await self.session.commit()
        await self.session.refresh(pet)
        
        return pet
    
    
    async def get_by_id(self, pet_id: int, owner_id: int) -> Pet | None:
        result = await self.session.execute(
            select(Pet).where(
                Pet.id == pet_id,
                Pet.owner_id == owner_id,    
            )
        )
        return result.scalar_one_or_none()
        
    async def list_for_owner(
        self,
        owner_id: int,
        filters: PetFilter,
        pagination: Pagination,
        ) -> list[Pet]:
        query = select(Pet).where(
                Pet.owner_id == owner_id
            )
        if filters.species is not None:
            query = query.where(
                Pet.species == filters.species
            )
        if filters.breed is not None:
            query = query.where(
                Pet.breed == filters.breed
            )
        if filters.max_weight is not None:
            query = query.where(
                Pet.weight <= filters.max_weight
            )
        if filters.min_weight is not None:
            query = query.where(
                Pet.weight >= filters.min_weight
            )
        if filters.name_contains is not None:
            query = query.where(
                Pet.name.ilike(f'%{filters.name_contains}%')
            )
        query = query.limit(pagination.page_size).offset(pagination.offset)
        result = await self.session.execute(query)        
        return list(result.scalars().all())
    
    async def update(self, pet: Pet, data: dict) -> Pet:
        for field, value in data.items():
            setattr(pet, field, value)
            
        await self.session.commit()
        await self.session.refresh(pet)
        
        return pet
    
    async def delete(self, pet: Pet) -> None:
        await self.session.delete(pet)
        await self.session.commit()