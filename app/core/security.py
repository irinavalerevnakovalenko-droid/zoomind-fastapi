from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
import jwt
from uuid import uuid4
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
        'type': 'access',
    }
    
    return jwt.encode(payload, settings.secret_key, algorithm=ALGORITHM)

def create_refresh_token(subject: str) -> tuple[str, str, datetime]:
    expire = datetime.now(timezone.utc) + timedelta(days=settings.refresh_token_expire_days)
    jti = str(uuid4())
    payload = {
        'sub': subject,
        'jti': jti,
        'exp': expire,
        'type': 'refresh',
    }
    token = jwt.encode(payload, settings.secret_key, algorithm=ALGORITHM)
    return token, jti, expire

def _decode_token(token: str, expected_type: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[ALGORITHM],
        )
    except jwt.PyJWTError:
        raise InvalidTokenError()

    if payload.get('type') != expected_type:
        raise InvalidTokenError()

    return payload


def decode_access_token(token: str) -> dict:
    return _decode_token(token, 'access')


def decode_refresh_token(token: str) -> dict:
    return _decode_token(token, 'refresh')
        
    
    
        