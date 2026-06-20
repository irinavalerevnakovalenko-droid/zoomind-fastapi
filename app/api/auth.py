from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.user import UserCreate, UserRead, TokenRead, UserLogin
from app.services.user import UserService
from app.core.dependencies import get_current_user, get_user_service
from app.models.user import User
from app.core.exceptions import (
    EmailAlreadyExistsError,
    InvalidCredentialsError,
    UsernameAlreadyExistsError,
)

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
    try:
        return await service.register_user(user_data)
    except EmailAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Пользователь с таким email уже существует',
        )
    except UsernameAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Пользователь с таким username уже существует',
        )

@router.post('/login', response_model=TokenRead)
async def login_user(
    login_data: UserLogin,
    service: UserService = Depends(get_user_service),
): 
    try:
        access_token = await service.login_user(login_data)
    except InvalidCredentialsError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Неверный логин или пароль',
        )
    
    return TokenRead(access_token=access_token)

@router.get('/me', response_model=UserRead)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user

