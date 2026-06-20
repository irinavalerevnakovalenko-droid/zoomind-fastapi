from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = 'Zoomind FastAPI'
    debug: bool = True
    
    database_url: str = 'postgresql+asyncpg://zoomind:zoomind@localhost:5432/zoomind'
    redis_url: str = 'redis://localhost:6379/0'
    
    
    secret_key: str = 'dev-secret-key'
    access_token_expire_minutes: int = 15
    
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
    )
    
settings = Settings()