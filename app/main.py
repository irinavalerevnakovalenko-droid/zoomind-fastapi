from fastapi import FastAPI

from app.api.health import router as health_router
from app.core.config import settings
from app.api.auth import router as auth_router
from app.api.pets import router as pets_router


app = FastAPI(
    title=settings.app_name,
    version='1.0.0',
)

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(pets_router)
