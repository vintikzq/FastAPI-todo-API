from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SECRET_KEY: str = "fallback_secret_key"
    DATABASE_URL: str = "sqlite:///./todos.db"
    ACCESS_TOKEN_EXPIRE: int = 30
    ALGORITHM: str = 'HS256'

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
