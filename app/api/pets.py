from fastapi import APIRouter, Depends, status

from app.core.dependencies import get_current_user, get_pet_service
from app.models.user import User
from app.schemas.pet import PetCreate, PetRead
from app.services.pet import PetService

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
    current_user: User = Depends(get_current_user),
    service: PetService = Depends(get_pet_service),
    ):

    return await service.list_pets(owner_id=current_user.id)

