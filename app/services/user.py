from datetime import UTC, datetime

from app.repositories.user import AbstractUserRepository
from app.schemas.user import UserCreate, UserLogin, UserUpdate
from app.services.security import AbstractSecurityService
from app.core.exceptions import (
    EmailAlreadyExistsError,
    InvalidCredentialsError,
    UsernameAlreadyExistsError,
    InvalidTokenError,
) 
from app.models.user import User
from app.repositories.refresh_token import AbstractRefreshTokenRepository


class UserService:
    def __init__(
        self,
        repository: AbstractUserRepository,
        security_service: AbstractSecurityService,
        refresh_token_repository: AbstractRefreshTokenRepository,
    ):
        self.repository = repository
        self.security_service = security_service
        self.refresh_token_repository = refresh_token_repository
        
    async def register_user(self, user_data: UserCreate):
        existing_email_user = await self.repository.get_by_email(user_data.email)
        if existing_email_user:
            raise EmailAlreadyExistsError()
            
        existing_username_user = await self.repository.get_by_username(
            user_data.username
        )
        if existing_username_user:
            raise UsernameAlreadyExistsError()
            
        hashed_password = self.security_service.hash_password(user_data.password)
        
        user = await self.repository.create(
            email=user_data.email,
            username=user_data.username,
            hashed_password=hashed_password,
            phone=user_data.phone,
            delivery_address=user_data.delivery_address,
            is_newsletter_enabled=user_data.is_newsletter_enabled,
        )
        
        return user
    
    async def login_user(self, login_data: UserLogin) -> tuple[str, str]:
        user = await self.repository.get_by_email(login_data.login)
        
        if user is None:
            user = await self.repository.get_by_username(login_data.login)
            
        if user is None:
            raise InvalidCredentialsError()
            
        if not self.security_service.verify_password(
            login_data.password,
            user.hashed_password,
        ):
            raise InvalidCredentialsError()

        access_token = self.security_service.create_access_token(
            subject=str(user.id),
        )
        refresh_token, jti, expires_at = (
            self.security_service.create_refresh_token(
                subject=str(user.id),
            )
        )
        await self.refresh_token_repository.create(
            user_id=user.id,
            jti=jti,
            expires_at=expires_at,
        )
        return access_token, refresh_token
    
    async def update_profile(
        self,
        user: User,
        user_data: UserUpdate,
        ) -> User:
        data = user_data.model_dump(exclude_unset=True)
        return await self.repository.update(user, data)
    
    async def refresh_tokens(
        self,
        refresh_token: str,
    ) -> tuple[str, str]:
        payload = self.security_service.decode_refresh_token(refresh_token)
        if 'sub' not in payload:
            raise InvalidTokenError()
        if 'jti' not in payload:
            raise InvalidTokenError()
        jti = payload['jti']
        stored_token = await self.refresh_token_repository.get_by_jti(jti)
        
        if stored_token is None:
            raise InvalidTokenError()
        
        try:
            user_id = int(payload['sub'])
        except (TypeError, ValueError):
            raise InvalidTokenError()
        if stored_token.user_id != user_id:
            raise InvalidTokenError()
        if (
            stored_token.revoked_at is not None
            or stored_token.expires_at <= datetime.now(UTC)
        ):
            raise InvalidTokenError()
        await self.refresh_token_repository.revoke(
            token=stored_token,
            revoked_at=datetime.now(UTC),
        )
        access_token = self.security_service.create_access_token(
            subject=str(user_id),
        )
        new_refresh_token, new_jti, new_expires_at = (
            self.security_service.create_refresh_token(
                subject=str(user_id),
            )
        )
        await self.refresh_token_repository.create(
            user_id=user_id,
            jti=new_jti,
            expires_at=new_expires_at,
        )
        
        return access_token, new_refresh_token
    
    
    async def logout(self, refresh_token: str) -> None:
        payload = self.security_service.decode_refresh_token(refresh_token)
        jti = payload.get('jti')

        if jti is None:
            raise InvalidTokenError()

        stored_token = await self.refresh_token_repository.get_by_jti(jti)

        if stored_token is None or stored_token.revoked_at is not None:
            raise InvalidTokenError()

        await self.refresh_token_repository.revoke(
            token=stored_token,
            revoked_at=datetime.now(UTC),
        )    
            
