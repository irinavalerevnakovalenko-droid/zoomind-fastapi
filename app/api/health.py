from fastapi import APIRouter, Depends
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
async def readyz(session: AsyncSession = Depends(get_db_session)):
    result = await session.execute(text('SELECT 1'))
    return {
        'status': 'ready',
        'database': result.scalar(),
    }
