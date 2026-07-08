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
from app.core.cache import CacheBackend

class ProductService:
    def __init__(
        self, 
        repository: AbstractProductRepository,
        cache: CacheBackend | None = None,
    ):
        self.repository = repository
        self.cache = cache
        
    def _build_catalog_cache_key(
        self,
        filters: ProductFilter,
        pagination: Pagination,
    ) -> str:
        return (
            'catalog:'
            f'category={filters.category}:'
            f'species={filters.species}:'
            f'name={filters.name_contains}:'
            f'min_price={filters.min_price}:'
            f'max_price={filters.max_price}:'
            f'in_stock={filters.in_stock}:'
            f'page={pagination.page}:'
            f'page_size={pagination.page_size}'
        )
        
    def _product_to_cache_data(self, product: Product) -> dict:
        return {
            'id': product.id,
            'sku': product.sku,
            'name': product.name,
            'category': product.category.value,
            'species': product.species.value,
            'price': str(product.price),
            'stock': product.stock,
            'description': product.description,
            'weight_kg': str(product.weight_kg) if product.weight_kg is not None else None,
        }
        
    async def _list_products_from_repository(
        self,
        filters: ProductFilter,
        pagination: Pagination,
    ) -> list[dict]:
        products = await self.repository.list(
            filters=filters,
            pagination=pagination,
        )

        return [
            self._product_to_cache_data(product)
            for product in products
        ]
        
    async def _invalidate_catalog_cache(self) -> None:
        if self.cache is not None:
            await self.cache.delete_by_prefix('catalog:')
        
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
        await self._invalidate_catalog_cache()
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
    ) -> list[dict]:
        if self.cache is None:
            return await self._list_products_from_repository(
                filters=filters,
                pagination=pagination,
            )

        cache_key = self._build_catalog_cache_key(filters, pagination)
        cached_products = await self.cache.get(cache_key)

        if cached_products is not None:
            return cached_products

        products = await self._list_products_from_repository(
            filters=filters,
            pagination=pagination,
        )

        await self.cache.set(cache_key, products, ttl=300)
        return products
        
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
            
        updated_product = await self.repository.update(product, data)
        await self._invalidate_catalog_cache()
        return updated_product
    
    async def delete_product(self, product_id: int) -> None:
        product = await self.get_product(product_id)
        await self.repository.delete(product)
        await self._invalidate_catalog_cache()