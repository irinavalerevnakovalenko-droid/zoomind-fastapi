from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    EmailAlreadyExistsError,
    UsernameAlreadyExistsError,
    InvalidCredentialsError,
    PetNotFoundError,
    InvalidTokenError,
    ProductNotFoundError,
    ProductSkuAlreadyExistsError,
    OrderNotFoundError,
    ProductOutOfStockError,
    InvalidOrderStatusTransitionError,
    InactiveUserError,
    AdminPermissionRequiredError,
)

def error_response(
    *,
    status_code: int,
    code: str,
    message: str,
    details: dict | None = None,
) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            'error': {
                'code': code,
                'message': message,
                'details': details or {},
            }
        },
    )

async def email_already_exists_handler(
    request: Request,
    exc: EmailAlreadyExistsError,
):
    return error_response(
        status_code=status.HTTP_400_BAD_REQUEST,
        code='EMAIL_ALREADY_EXISTS',
        message='Пользователь с таким email уже существует',
    )


async def username_already_exists_handler(
    request: Request,
    exc: UsernameAlreadyExistsError,
):
    return error_response(
        status_code=status.HTTP_400_BAD_REQUEST,
        code='USERNAME_ALREADY_EXISTS',
        message='Пользователь с таким username уже существует',
    )


async def invalid_credentials_handler(
    request: Request,
    exc: InvalidCredentialsError,
):
    return error_response(
        status_code=status.HTTP_401_UNAUTHORIZED,
        code='INVALID_CREDENTIALS',
        message='Неверный логин или пароль',
    )


async def invalid_token_handler(
    request: Request,
    exc: InvalidTokenError,
):
    return error_response(
        status_code=status.HTTP_401_UNAUTHORIZED,
        code='INVALID_TOKEN',
        message='Не удалось проверить токен',
    )

async def pet_not_found_handler(request: Request, exc: PetNotFoundError):
    return error_response(
        status_code=status.HTTP_404_NOT_FOUND,
        code='PET_NOT_FOUND',
        message='Питомец не найден',
    )
    
async def product_not_found_handler(request: Request, exc: ProductNotFoundError):
    return error_response(
        status_code=status.HTTP_404_NOT_FOUND,
        code='PRODUCT_NOT_FOUND',
        message='Товар не найден',
    )
    
async def product_sku_already_exists_handler(request: Request, exc: ProductSkuAlreadyExistsError):
    return error_response(
        status_code=status.HTTP_400_BAD_REQUEST,
        code='PRODUCT_SKU_ALREADY_EXISTS',
        message='Товар с таким артикулом уже существует',
    )
    
async def order_not_found_handler(request: Request, exc: OrderNotFoundError):
    return error_response(
        status_code=status.HTTP_404_NOT_FOUND,
        code='ORDER_NOT_FOUND',
        message='Заказ не найден',
    )
    
async def product_out_of_stock_handler(request: Request, exc: ProductOutOfStockError):
    return error_response(
        status_code=status.HTTP_400_BAD_REQUEST,
        code='PRODUCT_OUT_OF_STOCK',
        message='Недостаточно товара на складе',
    )
    
async def invalid_order_status_transition_handler(
    request: Request,
    exc: InvalidOrderStatusTransitionError,
):
    return error_response(
        status_code=status.HTTP_400_BAD_REQUEST,
        code='INVALID_ORDER_STATUS_TRANSITION',
        message='Недопустимый переход статуса заказа',
    )
    
async def inactive_user_handler(
    request: Request,
    exc: InactiveUserError,
):
    return error_response(
        status_code=status.HTTP_403_FORBIDDEN,
        code='INACTIVE_USER',
        message='Пользователь неактивен',
    )
    
async def admin_permission_required_handler(
    request: Request,
    exc: AdminPermissionRequiredError,
):
    return error_response(
        status_code=status.HTTP_403_FORBIDDEN,
        code='ADMIN_PERMISSION_REQUIRED',
        message='Для выполнения нужны права администратора',
    )