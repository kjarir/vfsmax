from typing import List, Optional, Union, Any
from pydantic import AnyHttpUrl, EmailStr, validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "VFSMAX"
    API_V1_STR: str = "/api/v1"
    
    JWT_SECRET: str = "vfsmax_default_secret_change_me"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    POSTGRES_SERVER: str = "db"
    POSTGRES_USER: str = "vfsmax"
    POSTGRES_PASSWORD: str = "vfsmax_pass"
    POSTGRES_DB: str = "vfsmax"
    SQLALCHEMY_DATABASE_URI: Optional[str] = None
    DATABASE_URL: Optional[str] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: dict) -> Any:
        if isinstance(v, str):
            return v
        return f"postgresql://{values.get('POSTGRES_USER')}:{values.get('POSTGRES_PASSWORD')}@{values.get('POSTGRES_SERVER')}/{values.get('POSTGRES_DB')}"

    REDIS_HOST: str = "redis"
    CELERY_BROKER_URL: Optional[str] = None
    CELERY_RESULT_BACKEND: Optional[str] = None

    @validator("CELERY_BROKER_URL", pre=True)
    def assemble_celery_broker(cls, v: Optional[str], values: dict) -> Any:
        if isinstance(v, str):
            return v
        return f"redis://{values.get('REDIS_HOST')}:6379/0"

    OPENAI_API_KEY: str = ""
    TWOCAPTCHA_API_KEY: Optional[str] = None
    TELEGRAM_BOT_TOKEN: Optional[str] = None
    TELEGRAM_CHAT_ID: Optional[str] = None
    
    VFSMAX_ENCRYPTION_KEY: str = "vfsmax_encryption_key_32bytes_exactly" # Used for AES-256
    
    # Stealth Settings
    MAX_CONCURRENT_WORKERS: int = 5
    DEFAULT_CHECK_INTERVAL: int = 300  # seconds
    AUTO_BOOK_THRESHOLD: int = 85
    
    model_config = SettingsConfigDict(case_sensitive=True, env_file=".env")


settings = Settings()
