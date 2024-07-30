from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "DATA INTEGRATION POC"
    SECRET_KEY: str = "secret-key"
    API_PREFIX: str = "/v1"
    SQLALCHEMY_DATABASE_URI: str = "sqlite+aiosqlite:///./data_integration.db"
    DEBUG: bool = False
    
    class Config:
        case_sensitive = True
        env_file = ".env"  # Specify the .env file


settings = Settings()
