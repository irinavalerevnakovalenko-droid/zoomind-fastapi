from fastapi import APIRouter, Depends, status

from app.core.dependencies import get_current_user, get_pet_service
from app.models.user import User
from app.schemas.pet import PetCreate, PetRead, PetUpdate, PetFilter
from app.services.pet import PetService
from app.schemas.pagination import Pagination

router = APIRouter(
    prefix='/pets',
    tags=['pets'],
)
@router.post(
    '/',
    response_model=PetRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_pet(
    pet_data: PetCreate,
    current_user: User = Depends(get_current_user),
    service: PetService = Depends(get_pet_service),  
):
    return await service.create_pet(
        owner_id=current_user.id,
        pet_data=pet_data,
    )
    
@router.get(
    '/',
    response_model=list[PetRead],
    status_code=status.HTTP_200_OK,
)
async def list_pets(
    filters: PetFilter = Depends(),
    pagination: Pagination = Depends(),
    current_user: User = Depends(get_current_user),
    service: PetService = Depends(get_pet_service),
    ):

    return await service.list_pets(
        owner_id=current_user.id,
        filters=filters,
        pagination=pagination,
    )

@router.get(
    '/{pet_id}',
    response_model=PetRead,
    status_code=status.HTTP_200_OK,
)
async def get_pet(
    pet_id: int,
    current_user: User = Depends(get_current_user),
    service: PetService = Depends(get_pet_service),
    ):
    
    return await service.get_pet(
        pet_id=pet_id,
        owner_id=current_user.id,
    )
    
    
@router.patch(
    '/{pet_id}',
    response_model=PetRead,
    status_code=status.HTTP_200_OK,
) 
async def update_pet(
    pet_id: int,
    pet_data: PetUpdate,
    current_user: User = Depends(get_current_user),
    service: PetService = Depends(get_pet_service),
):
    
    return await service.update_pet(
        pet_id=pet_id,
        owner_id=current_user.id,
        pet_data=pet_data,
    )
    
@router.delete(
    '/{pet_id}',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_pet(
    pet_id: int,
    current_user: User = Depends(get_current_user),
    service: PetService = Depends(get_pet_service),
):
    await service.delete_pet(
        pet_id=pet_id,
        owner_id=current_user.id,
    )
    