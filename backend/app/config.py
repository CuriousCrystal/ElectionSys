from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # MongoDB
    mongodb_uri: str = "mongodb://localhost:27017"
    database_name: str = "election_assistant"
    
    # JWT Authentication
    jwt_secret_key: str = "fallback-secret-change-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    
    # AI Assistant
    xai_api_key: str = ""
    
    # Server
    cors_origins: List[str] = ["http://localhost:5173"]
    rate_limit_max_requests: int = 120
    rate_limit_window_seconds: int = 60
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
