import json
from typing import List, Union
from pydantic import field_validator
from pydantic_settings import BaseSettings


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
    
    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: Union[str, List[str], None]) -> List[str]:
        if value is None:
            return ["http://localhost:5173"]
        if isinstance(value, list):
            return value
        if isinstance(value, str):
            if not value.strip():
                return ["http://localhost:5173"]
            try:
                parsed = json.loads(value)
                if isinstance(parsed, list):
                    return [str(item) for item in parsed]
            except json.JSONDecodeError:
                pass
            return [item.strip() for item in value.split(",") if item.strip()]
        return ["http://localhost:5173"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
