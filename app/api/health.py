from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from sqlalchemy import text

router = APIRouter(
    tags=['health'],
)

@router.get('/healthz')
async def healthz():
    return {'status': 'ok'}

@router.get('/readyz')
async def readyz(request: Request, session: AsyncSession = Depends(get_db_session)):
    db_result = await session.execute(text('SELECT 1'))
    redis_result = await request.app.state.redis.ping()
    
    return {
        'status': 'ready',
        'database': db_result.scalar(),
        'redis': redis_result,
    }
