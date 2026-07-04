from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from sqlalchemy import text
from redis.asyncio import Redis
from app.core.config import settings

router = APIRouter(
    tags=['health'],
)

@router.get('/healthz')
async def healthz():
    return {'status': 'ok'}

@router.get('/readyz')
async def readyz(session: AsyncSession = Depends(get_db_session)):
    db_result = await session.execute(text('SELECT 1'))
    redis = Redis.from_url(settings.redis_url)
    redis_result = await redis.ping()
    await redis.aclose()
    
    return {
        'status': 'ready',
        'database': db_result.scalar(),
        'redis': redis_result,
    }
