from fastapi import APIRouter, Depends, status
from fastapi import Response, Request

from app.schemas.user import UserCreate, UserRead, TokenRead, UserLogin, UserUpdate
from app.services.user import UserService
from app.core.dependencies import (
    get_current_active_user, 
    get_user_service,
    throttle_user,
)
from app.core.config import settings
from app.models.user import User
from app.core.exceptions import InvalidTokenError


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
    response: Response,
    service: UserService = Depends(get_user_service),
):
    access_token, refresh_token = await service.login_user(login_data)
    response.set_cookie(
        key='refresh_token',
        value=refresh_token,
        httponly=True,
        samesite='lax',
        secure=not settings.debug,
        max_age=settings.refresh_token_expire_days * 24 * 60 * 60,
        path='/api/v1/auth',
    )

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
    
@router.post('/refresh', response_model=TokenRead)
async def refresh_access_token(
    request: Request,
    response: Response,
    service: UserService = Depends(get_user_service),
):
    refresh_token = request.cookies.get('refresh_token')
    
    if refresh_token is None:
        raise InvalidTokenError()
    
    access_token, new_refresh_token = await service.refresh_tokens(
        refresh_token,
    )
    
    response.set_cookie(
        key='refresh_token',
        value=new_refresh_token,
        httponly=True,
        samesite='lax',
        secure=not settings.debug,
        max_age=settings.refresh_token_expire_days * 24 * 60 * 60,
        path='/api/v1/auth',
    )

    return TokenRead(access_token=access_token)

@router.post(
    '/logout',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def logout(
    request: Request,
    response: Response,
    service: UserService = Depends(get_user_service),
):
    refresh_token = request.cookies.get('refresh_token')

    if refresh_token is not None:
        await service.logout(refresh_token)

    response.delete_cookie(
        key='refresh_token',
        path='/api/v1/auth',
        httponly=True,
        samesite='lax',
        secure=not settings.debug,
    )

