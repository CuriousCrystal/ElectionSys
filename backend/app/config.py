import json
import os
from typing import List, Union, Optional
from pydantic import field_validator
from pydantic_settings import BaseSettings

try:
    from google.cloud import secretmanager
except ImportError:
    secretmanager = None


def get_secret(project_id: str, secret_id: str) -> Optional[str]:
    """Fetch secret from Google Cloud Secret Manager"""
    if not secretmanager or not project_id:
        return None
    try:
        client = secretmanager.SecretManagerServiceClient()
        name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
        response = client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")
    except Exception:
        # Fallback to env var if secret fetching fails
        return None


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Cloud settings
    gcp_project_id: str = ""
    gcp_credentials_path: str = ""
    
    # Secret IDs
    xai_api_key_secret_id: str = "XAI_API_KEY"

    # AI Assistant
    xai_api_key: str = ""

    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    cors_origins: List[str] = ["http://localhost:5173"]
    rate_limit_max_requests: int = 120
    rate_limit_window_seconds: int = 60

    def __init__(self, **values):
        super().__init__(**values)
        # If API key is missing, try to fetch from Secret Manager
        if not self.xai_api_key and self.gcp_project_id:
            secret = get_secret(self.gcp_project_id, self.xai_api_key_secret_id)
            if secret:
                self.xai_api_key = secret

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
        extra = "ignore" # Allow extra fields like HOST and PORT without crashing


settings = Settings()
