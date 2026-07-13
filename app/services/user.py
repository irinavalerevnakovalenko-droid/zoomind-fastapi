
from app.repositories.user import AbstractUserRepository
from app.schemas.user import UserCreate, UserLogin, UserUpdate
from app.services.security import AbstractSecurityService
from app.core.exceptions import (
    EmailAlreadyExistsError,
    InvalidCredentialsError,
    UsernameAlreadyExistsError,
) 
from app.models.user import User


class UserService:
    def __init__(
        self,
        repository: AbstractUserRepository,
        security_service: AbstractSecurityService,
    ):
        self.repository = repository
        self.security_service = security_service
        
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
    
    async def login_user(self, login_data: UserLogin) -> str:
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

        return self.security_service.create_access_token(subject=str(user.id))
    
    async def update_profile(
        self,
        user: User,
        user_data: UserUpdate,
        ) -> User:
        data = user_data.model_dump(exclude_unset=True)
        return await self.repository.update(user, data)
