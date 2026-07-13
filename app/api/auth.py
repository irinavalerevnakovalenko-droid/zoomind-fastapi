from fastapi import APIRouter, Depends, status

from app.schemas.user import UserCreate, UserRead, TokenRead, UserLogin, UserUpdate
from app.services.user import UserService
from app.core.dependencies import (
    get_current_active_user, 
    get_user_service,
    throttle_user,
)
from app.models.user import User


router = APIRouter(
    prefix='/auth',
    tags=['auth'],
)

@router.post(
    '/register',
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    user_data: UserCreate,
    service: UserService = Depends(get_user_service),
):
    return await service.register_user(user_data)

@router.post('/login', response_model=TokenRead)
async def login_user(
    login_data: UserLogin,
    service: UserService = Depends(get_user_service),
):
    access_token = await service.login_user(login_data)
    return TokenRead(access_token=access_token)


@router.get('/me', response_model=UserRead)
async def get_me(
    current_user: User = Depends(get_current_active_user),
    _: None = Depends(throttle_user),
):
    return current_user

@router.patch(
    '/me', 
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
    )
async def update_me(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    _: None = Depends(throttle_user),
    service: UserService = Depends(get_user_service),
):
    return await service.update_profile(
        user=current_user,
        user_data=user_data,
    )
