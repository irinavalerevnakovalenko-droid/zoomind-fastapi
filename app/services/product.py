from app.core.exceptions import (
    ProductNotFoundError,
    ProductSkuAlreadyExistsError,
)
from app.models.product import Product
from app.repositories.product import AbstractProductRepository
from app.schemas.pagination import Pagination
from app.schemas.product import (
    ProductCreate,
    ProductFilter,
    ProductUpdate,
)

class ProductService:
    def __init__(self, repository: AbstractProductRepository):
        self.repository = repository
        
    async def create_product(self, product_data: ProductCreate) -> Product:
        existing_product = await self.repository.get_by_sku(product_data.sku)
        
        if existing_product:
            raise ProductSkuAlreadyExistsError()
        
        product = await self.repository.create(
            sku=product_data.sku,
            name=product_data.name,
            category=product_data.category,
            species=product_data.species,
            price=product_data.price,
            stock=product_data.stock,
            description=product_data.description,
            weight_kg=product_data.weight_kg,  
        )
        return product
    
    async def get_product(self, product_id: int) -> Product:
        product = await self.repository.get_by_id(product_id)
        
        if product is None:
            raise ProductNotFoundError()
        
        
        return product
    
    async def list_products(
        self, 
        filters: ProductFilter,
        pagination: Pagination,
        ) -> list[Product]:
        return await self.repository.list(
            filters=filters,
            pagination=pagination,
        )
        
    async def update_product(
        self, 
        product_id: int,
        product_data: ProductUpdate,
        ) -> Product:
        product = await self.get_product(product_id)
        data = product_data.model_dump(exclude_unset=True)
        if 'sku' in data:
            existing_product = await self.repository.get_by_sku(data['sku'])
            if existing_product is not None and existing_product.id != product.id:
                raise ProductSkuAlreadyExistsError()
        return await self.repository.update(product, data)
    
    async def delete_product(self, product_id: int) -> None:
        product = await self.get_product(product_id)
        await self.repository.delete(product)