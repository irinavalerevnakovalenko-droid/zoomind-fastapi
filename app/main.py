from fastapi import FastAPI

from app.api.health import router as health_router
from app.core.config import settings
from app.core.exceptions import (
    EmailAlreadyExistsError,
    InvalidCredentialsError,
    InvalidTokenError,
    PetNotFoundError,
    UsernameAlreadyExistsError,
)
from app.core.exception_handlers import (
    email_already_exists_handler,
    invalid_credentials_handler,
    invalid_token_handler,
    pet_not_found_handler,
    username_already_exists_handler,
)
from app.api.auth import router as auth_router
from app.api.pets import router as pets_router


app = FastAPI(
    title=settings.app_name,
    version='1.0.0',
)

app.add_exception_handler(EmailAlreadyExistsError, email_already_exists_handler)
app.add_exception_handler(UsernameAlreadyExistsError, username_already_exists_handler)
app.add_exception_handler(InvalidCredentialsError, invalid_credentials_handler)
app.add_exception_handler(InvalidTokenError, invalid_token_handler)
app.add_exception_handler(PetNotFoundError, pet_not_found_handler)

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(pets_router)



