from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
import jwt
from app.core.exceptions import InvalidTokenError

from app.core.config import settings


password_hash = PasswordHash.recommended()

def hash_password(password: str) -> str:
    return password_hash.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)

ALGORITHM = 'HS256'

def create_access_token(subject: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    
    payload = {
        'sub': subject,
        'exp': expire,
    }
    
    return jwt.encode(payload, settings.secret_key, algorithm=ALGORITHM)

def decode_access_token(token: str) -> dict:
    try:
        return jwt.decode(
            token,
            settings.secret_key,
            algorithms=[ALGORITHM],
        )
        
    except jwt.PyJWTError:
        raise InvalidTokenError()
        