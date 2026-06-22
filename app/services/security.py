from typing import Protocol

from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)

class AbstractSecurityService(Protocol):
    def hash_password(self, password: str) -> str:
        ...

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        ...

    def create_access_token(self, subject: str) -> str:
        ...


class SecurityService:
    def hash_password(self, password: str) -> str:
        return hash_password(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return verify_password(plain_password, hashed_password)

    def create_access_token(self, subject: str) -> str:
        return create_access_token(subject)