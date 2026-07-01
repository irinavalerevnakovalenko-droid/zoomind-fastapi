from decimal import Decimal
from typing import Protocol

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import ProductCategory, ProductSpecies
from app.models.product import Product
from app.schemas.pagination import Pagination
from app.schemas.product import ProductFilter

class AbstractProductRepository(Protocol):
    async def create(
        self,
        *,
        sku: str,
        name: str,
        category: ProductCategory,
        species: ProductSpecies,
        price: Decimal,
        stock: int,
        description: str,
        weight_kg: Decimal | None,
    ) -> Product:
        ...
        
    async def get_by_id(self, product_id: int) -> Product | None:
        ...

    async def get_by_sku(self, sku: str) -> Product | None:
        ...

    async def list(
        self,
        filters: ProductFilter,
        pagination: Pagination,
    ) -> list[Product]:
        ...

    async def update(self, product: Product, data: dict) -> Product:
        ...

    async def delete(self, product: Product) -> None:
        ...
        


class SQLAlchemyProductRepository(AbstractProductRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def create(
        self,
        *,
        sku: str,
        name: str,
        category: ProductCategory,
        species: ProductSpecies,
        price: Decimal,
        stock: int,
        description: str,
        weight_kg: Decimal | None,
    ) -> Product:
        product = Product(
            sku=sku,
            name=name,
            category=category,
            species=species,
            price=price,
            stock=stock,
            description=description,
            weight_kg=weight_kg,  
            )
        
        self.session.add(product)
        await self.session.commit()
        await self.session.refresh(product)
        
        return product
    
    
    async def get_by_id(self, product_id: int) -> Product | None:
        result = await self.session.execute(
            select(Product).where(
                Product.id == product_id,  
            )
        )
        return result.scalar_one_or_none()
    
    async def get_by_sku(self, sku: str) -> Product | None:
        result = await self.session.execute(
            select(Product).where(
                Product.sku == sku,  
            )
        )
        return result.scalar_one_or_none()
    
    async def list(
        self,
        filters: ProductFilter,
        pagination: Pagination,
        ) -> list[Product]:
        query = select(Product)
        if filters.category is not None:
            query = query.where(
                Product.category == filters.category
            )
        if filters.species is not None:
            query = query.where(
                Product.species == filters.species
            )
        if filters.max_price is not None:
            query = query.where(
                Product.price <= filters.max_price
            )
        if filters.min_price is not None:
            query = query.where(
                Product.price >= filters.min_price
            )
        if filters.name_contains is not None:
            query = query.where(
                Product.name.ilike(f'%{filters.name_contains}%')
            )
        if filters.in_stock is True:
            query = query.where(Product.stock > 0)
            
        query = query.limit(pagination.page_size).offset(pagination.offset)
        result = await self.session.execute(query)        
        return list(result.scalars().all())
    
    async def update(self, product: Product, data: dict) -> Product:
        for field, value in data.items():
            setattr(product, field, value)

        await self.session.commit()
        await self.session.refresh(product)

        return product
    
    async def delete(self, product: Product) -> None:
        await self.session.delete(product)
        await self.session.commit()


    
