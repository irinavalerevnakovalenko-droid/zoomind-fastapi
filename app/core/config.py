from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = 'Zoomind FastAPI'
    debug: bool = True
    
    database_url: str = 'postgresql+asyncpg://zoomind:zoomind@localhost:5432/zoomind'
    redis_url: str = 'redis://localhost:6379/0'
    celery_broker_url: str = 'redis://localhost:6379/1'
    celery_result_backend: str = 'redis://localhost:6379/2'
    rate_limit_requests: int = 60
    rate_limit_window_seconds: int = 60
    
    
    secret_key: str = 'dev-secret-key'
    access_token_expire_minutes: int = 15
    
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
    )
    
settings = Settings()