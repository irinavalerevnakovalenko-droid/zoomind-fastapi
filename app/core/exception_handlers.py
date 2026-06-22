from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    EmailAlreadyExistsError,
    UsernameAlreadyExistsError,
    InvalidCredentialsError,
    PetNotFoundError,
    InvalidTokenError,
)

async def email_already_exists_handler(
    request: Request,
    exc: EmailAlreadyExistsError,
):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={'detail': 'Пользователь с таким email уже существует'},
    )


async def username_already_exists_handler(
    request: Request,
    exc: UsernameAlreadyExistsError,
):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={'detail': 'Пользователь с таким username уже существует'},
    )


async def invalid_credentials_handler(
    request: Request,
    exc: InvalidCredentialsError,
):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={'detail': 'Неверный логин или пароль'},
    )


async def invalid_token_handler(
    request: Request,
    exc: InvalidTokenError,
):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={'detail': 'Не удалось проверить токен'},
    )

async def pet_not_found_handler(request: Request, exc: PetNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={'detail': 'Питомец не найден'},
    )
    