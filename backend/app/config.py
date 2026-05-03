from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Cloud settings
    gcp_project_id: str = ""
    gcp_credentials_path: str = ""
    
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
