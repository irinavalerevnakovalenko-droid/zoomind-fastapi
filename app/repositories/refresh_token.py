from typing import Protocol
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.refresh_token import RefreshToken

class AbstractRefreshTokenRepository(Protocol):
    async def create(
        self,
        *,
        user_id: int,
        jti: str,
        expires_at: datetime,
    ) -> RefreshToken:
        ...
        
    async def get_by_jti(self, jti: str) -> RefreshToken | None:
        ...

    async def revoke(
        self,
        token: RefreshToken,
        revoked_at: datetime,
    ) -> RefreshToken:
        ...
        
class SQLAlchemyRefreshTokenRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def create(
        self,
        *,
        user_id: int,
        jti: str,
        expires_at: datetime,
    ) -> RefreshToken:
        refresh_token = RefreshToken(
            user_id=user_id,
            jti=jti,
            expires_at=expires_at,
        )

        self.session.add(refresh_token)
        await self.session.commit()
        await self.session.refresh(refresh_token)
        
        return refresh_token
    
    async def get_by_jti(self, jti: str) -> RefreshToken | None:
        result = await self.session.execute(
            select(RefreshToken).where(RefreshToken.jti == jti)
        )
        return result.scalar_one_or_none()
    
    async def revoke(
        self,
        token: RefreshToken,
        revoked_at: datetime,
    ) -> RefreshToken:
        token.revoked_at = revoked_at

        await self.session.commit()
        await self.session.refresh(token)
        
        return token
        