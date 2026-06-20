from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.core.security import decode_access_token
from app.models.user import User

from app.repositories.user import UserRepository
from app.services.user import UserService
from app.repositories.pet import AbstractPetRepository, SQLAlchemyPetRepository
from app.services.pet import PetService

bearer_scheme = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    session: AsyncSession = Depends(get_db_session),
) -> User:
    payload = decode_access_token(credentials.credentials)
    
    user_id = payload.get('sub')
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='В токене нет пользователя',
        )
        
    repository = UserRepository(session)
    user = await repository.get_by_id(int(user_id))
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Пользователь не найден',
        )

    return user

def get_user_repository(
    session: AsyncSession = Depends(get_db_session),
) -> UserRepository:
    return UserRepository(session)

def get_user_service(
    repository: UserRepository = Depends(get_user_repository),
) -> UserService:
    return UserService(repository)

def get_pet_repository(
    session: AsyncSession = Depends(get_db_session),
) -> AbstractPetRepository:
    return SQLAlchemyPetRepository(session)

def get_pet_service(
    repository: AbstractPetRepository = Depends(get_pet_repository),
) -> PetService:
    return PetService(repository)