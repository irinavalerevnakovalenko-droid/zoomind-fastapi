from typing import Protocol

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User

class AbstractUserRepository(Protocol):
    async def get_by_email(self, email: str) -> User | None:
        ...

    async def get_by_username(self, username: str) -> User | None:
        ...

    async def create(
        self,
        *,
        email: str,
        username: str,
        hashed_password: str,
        phone: str,
        delivery_address: str,
        is_newsletter_enabled: bool,
    ) -> User:
        ...

    async def get_by_id(self, user_id: int) -> User | None:
        ...
        
    async def update(self, user: User, data: dict) -> User:
        ...
    

class UserRepository(AbstractUserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def get_by_email(self, email: str) -> User | None:
        result = await self.session.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()
    
    async def get_by_username(self, username: str) -> User | None:
        result = await self.session.execute(
            select(User).where(User.username == username)
        )
        return result.scalar_one_or_none()
    
    async def create(
        self,
        *,
        email: str,
        username: str,
        hashed_password: str,
        phone: str,
        delivery_address: str,
        is_newsletter_enabled: bool,
    ) -> User:
        user = User(
            email=email,
            username=username,
            hashed_password=hashed_password,
            phone=phone,
            delivery_address=delivery_address,
            is_newsletter_enabled=is_newsletter_enabled,
        )
        
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        
        return user
    
    async def get_by_id(self, user_id: int) -> User | None:
        result = await self.session.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()
    
    async def update(self, user: User, data: dict) -> User:
        for field, value in data.items():
            setattr(user, field, value)
    
        await self.session.commit()
        await self.session.refresh(user)

        return user
    
    
