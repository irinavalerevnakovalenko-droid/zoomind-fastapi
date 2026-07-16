from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis
from collections.abc import AsyncGenerator

from app.core.database import get_db_session
from app.core.security import decode_access_token
from app.core.exceptions import (
    InvalidTokenError, 
    InactiveUserError, 
    AdminPermissionRequiredError,
    TooManyRequestsError,
)
from app.core.config import settings
from app.core.cache import CacheBackend, RedisCacheBackend


from app.models.user import User
from app.models.pet import Pet

from app.repositories.user import UserRepository
from app.services.user import UserService
from app.services.security import AbstractSecurityService, SecurityService
from app.repositories.pet import AbstractPetRepository, SQLAlchemyPetRepository
from app.services.pet import PetService
from app.repositories.product import AbstractProductRepository, SQLAlchemyProductRepository
from app.services.product import ProductService
from app.repositories.order import AbstractOrderRepository, SQLAlchemyOrderRepository
from app.services.order import OrderService
from app.repositories.refresh_token import AbstractRefreshTokenRepository, SQLAlchemyRefreshTokenRepository

bearer_scheme = HTTPBearer()

def get_security_service() -> AbstractSecurityService:
    return SecurityService()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    session: AsyncSession = Depends(get_db_session),
) -> User:
    payload = decode_access_token(credentials.credentials)
    
    user_id = payload.get('sub')
    if user_id is None:
        raise InvalidTokenError()
        
    repository = UserRepository(session)
    user = await repository.get_by_id(int(user_id))
    
    if user is None:
        raise InvalidTokenError()

    return user

async def get_current_active_user(
    user: User = Depends(get_current_user),
) -> User:
    if not user.is_active:
        raise InactiveUserError()
    return user

async def get_admin_user(
    user: User = Depends(get_current_active_user),
) -> User:
    if not user.is_admin:
        raise AdminPermissionRequiredError()
    return user

def get_refresh_token_repository(
    session: AsyncSession = Depends(get_db_session),
) -> AbstractRefreshTokenRepository:
    return SQLAlchemyRefreshTokenRepository(session)

def get_user_repository(
    session: AsyncSession = Depends(get_db_session),
) -> UserRepository:
    return UserRepository(session)

def get_user_service(
    repository: UserRepository = Depends(get_user_repository),
    security_service: AbstractSecurityService = Depends(get_security_service),
    refresh_token_repository: AbstractRefreshTokenRepository = Depends(get_refresh_token_repository),
) -> UserService:
    return UserService(
        repository=repository,
        security_service=security_service,
        refresh_token_repository=refresh_token_repository,
    )

def get_pet_repository(
    session: AsyncSession = Depends(get_db_session),
) -> AbstractPetRepository:
    return SQLAlchemyPetRepository(session)

def get_pet_service(
    repository: AbstractPetRepository = Depends(get_pet_repository),
) -> PetService:
    return PetService(repository)

async def get_cache() -> AsyncGenerator[CacheBackend, None]:
    redis = Redis.from_url(settings.redis_url)
    
    try:
        yield RedisCacheBackend(redis)
    finally:
        await redis.aclose()
        
async def throttle_user(
    current_user: User = Depends(get_current_active_user),
) -> None:
    redis = Redis.from_url(settings.redis_url)
    key = f'rate_limit:user:{current_user.id}'

    try:
        requests_count = await redis.incr(key)

        if requests_count == 1:
            await redis.expire(key, settings.rate_limit_window_seconds)

        if requests_count > settings.rate_limit_requests:
            raise TooManyRequestsError()
    finally:
        await redis.aclose()
        
async def get_pet_for_owner(
    pet_id: int,
    current_user: User = Depends(get_current_active_user),
    service: PetService = Depends(get_pet_service),
) -> Pet:
    return await service.get_pet(
        pet_id=pet_id,
        owner_id=current_user.id,
    )

def get_product_repository(
    session: AsyncSession = Depends(get_db_session),
) -> AbstractProductRepository:
    return SQLAlchemyProductRepository(session)

def get_product_service(
    repository: AbstractProductRepository = Depends(get_product_repository),
    cache: CacheBackend = Depends(get_cache),
) -> ProductService:
    return ProductService(
        repository=repository,
        cache=cache,
    )

def get_order_repository(
    session: AsyncSession = Depends(get_db_session),
) -> AbstractOrderRepository:
    return SQLAlchemyOrderRepository(session)

def get_order_service(
    order_repository: AbstractOrderRepository = Depends(get_order_repository),
    product_repository: AbstractProductRepository = Depends(get_product_repository),
) -> OrderService:
    return OrderService(
        order_repository=order_repository,
        product_repository=product_repository,
    )
    

    
