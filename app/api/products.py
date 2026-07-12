from fastapi import APIRouter, Depends, status

from app.core.dependencies import (
    get_product_service,
    get_admin_user, 
    throttle_user,
)
from app.schemas.product import ProductCreate, ProductRead, ProductUpdate, ProductFilter
from app.services.product import ProductService
from app.schemas.pagination import Pagination
from app.models.user import User

router = APIRouter(
    prefix='/products',
    tags=['products'],
)
@router.post(
    '/',
    response_model=ProductRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_product(
    product_data: ProductCreate,
    admin_user: User = Depends(get_admin_user),
    _: None = Depends(throttle_user),
    service: ProductService = Depends(get_product_service),  
):
    return await service.create_product(
        product_data=product_data,
    )
    
@router.get(
    '/',
    response_model=list[ProductRead],
    status_code=status.HTTP_200_OK,
)
async def list_products(
    filters: ProductFilter = Depends(),
    pagination: Pagination = Depends(),
    service: ProductService = Depends(get_product_service),
    ):

    return await service.list_products(
        filters=filters,
        pagination=pagination,
    )
    
@router.get(
    '/{product_id}',
    response_model=ProductRead,
    status_code=status.HTTP_200_OK,
)
async def get_product(
    product_id: int,
    service: ProductService = Depends(get_product_service),
    ):
    
    return await service.get_product(
        product_id=product_id,
    )
    
@router.patch(
    '/{product_id}',
    response_model=ProductRead,
    status_code=status.HTTP_200_OK,
) 
async def update_product(
    product_id: int,
    product_data: ProductUpdate,
    admin_user: User = Depends(get_admin_user),
    _: None = Depends(throttle_user),
    service: ProductService = Depends(get_product_service),
):
    
    return await service.update_product(
        product_id=product_id,
        product_data=product_data,
    )
    
@router.delete(
    '/{product_id}',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_product(
    product_id: int,
    admin_user: User = Depends(get_admin_user),
    _: None = Depends(throttle_user),
    service: ProductService = Depends(get_product_service),
):
    await service.delete_product(
        product_id=product_id,
    )