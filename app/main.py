from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

from contextlib import asynccontextmanager

from redis.asyncio import Redis
from sqlalchemy import text

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
    AdminPermissionRequiredError,
    TooManyRequestsError,
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
    admin_permission_required_handler,
    too_many_requests_handler,
)
from app.core.database import engine

from app.api.auth import router as auth_router
from app.api.pets import router as pets_router
from app.api.products import router as products_router
from app.api.orders import router as orders_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = Redis.from_url(settings.redis_url)
    
    try:
        await redis.ping()
        
        async with engine.connect() as connection:
            await connection.execute(text('SELECT 1'))
            
        app.state.redis = redis
        
        yield
    finally:
        await redis.aclose()
        await engine.dispose()
        

app = FastAPI(
    title=settings.app_name,
    version='1.0.0',
    lifespan=lifespan,
)

app.add_middleware(
    GZipMiddleware,
    minimum_size=500,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'PATCH', 'DELETE', 'OPTIONS'],
    allow_headers=['Authorization', 'Content-Type'],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.trusted_hosts,
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
app.add_exception_handler(
    AdminPermissionRequiredError,
    admin_permission_required_handler,
)
app.add_exception_handler(TooManyRequestsError, too_many_requests_handler)

app.include_router(health_router)
app.include_router(auth_router, prefix='/api/v1')
app.include_router(pets_router, prefix='/api/v1')
app.include_router(products_router, prefix='/api/v1')
app.include_router(orders_router, prefix='/api/v1')



