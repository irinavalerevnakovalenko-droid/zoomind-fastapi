from typing import Protocol
from datetime import datetime

from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
    create_refresh_token,
    decode_refresh_token,
)

class AbstractSecurityService(Protocol):
    def hash_password(self, password: str) -> str:
        ...

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        ...

    def create_access_token(self, subject: str) -> str:
        ...
        
    def create_refresh_token(
        self,
        subject: str,
    ) -> tuple[str, str, datetime]:
        ...

    def decode_refresh_token(self, token: str) -> dict:
        ...


class SecurityService:
    def hash_password(self, password: str) -> str:
        return hash_password(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return verify_password(plain_password, hashed_password)

    def create_access_token(self, subject: str) -> str:
        return create_access_token(subject)
    
    def create_refresh_token(
        self,
        subject: str,
    ) -> tuple[str, str, datetime]:
        return create_refresh_token(subject)
    
    def decode_refresh_token(self, token: str) -> dict:
        return decode_refresh_token(token)
    
    