from fastapi import FastAPI

from app.api.health import router as health_router
from app.core.config import settings
from app.core.exceptions import (
    EmailAlreadyExistsError,
    InvalidCredentialsError,
    InvalidTokenError,
    PetNotFoundError,
    UsernameAlreadyExistsError,
    ProductNotFoundError,
    ProductSkuAlreadyExistsError,
    OrderNotFoundError,
    ProductOutOfStockError,
    InvalidOrderStatusTransitionError,
    InactiveUserError,
)
from app.core.exception_handlers import (
    email_already_exists_handler,
    invalid_credentials_handler,
    invalid_token_handler,
    pet_not_found_handler,
    username_already_exists_handler,
    product_not_found_handler,
    product_sku_already_exists_handler,
    order_not_found_handler,
    product_out_of_stock_handler,
    invalid_order_status_transition_handler,
    inactive_user_handler,
)
from app.api.auth import router as auth_router
from app.api.pets import router as pets_router
from app.api.products import router as products_router
from app.api.orders import router as orders_router


app = FastAPI(
    title=settings.app_name,
    version='1.0.0',
)

app.add_exception_handler(EmailAlreadyExistsError, email_already_exists_handler)
app.add_exception_handler(UsernameAlreadyExistsError, username_already_exists_handler)
app.add_exception_handler(InvalidCredentialsError, invalid_credentials_handler)
app.add_exception_handler(InvalidTokenError, invalid_token_handler)
app.add_exception_handler(InactiveUserError, inactive_user_handler)
app.add_exception_handler(PetNotFoundError, pet_not_found_handler)
app.add_exception_handler(ProductNotFoundError, product_not_found_handler)
app.add_exception_handler(ProductSkuAlreadyExistsError, product_sku_already_exists_handler)
app.add_exception_handler(OrderNotFoundError, order_not_found_handler)
app.add_exception_handler(ProductOutOfStockError, product_out_of_stock_handler)
app.add_exception_handler(
    InvalidOrderStatusTransitionError,
    invalid_order_status_transition_handler,
)

app.include_router(health_router)
app.include_router(auth_router, prefix='/api/v1')
app.include_router(pets_router, prefix='/api/v1')
app.include_router(products_router, prefix='/api/v1')
app.include_router(orders_router, prefix='/api/v1')



