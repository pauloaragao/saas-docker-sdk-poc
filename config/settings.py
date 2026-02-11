"""
Application settings and configuration
"""
import os
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # API Configuration
    api_title: str = os.getenv("API_TITLE", "SaaS API")
    api_version: str = os.getenv("API_VERSION", "0.1.0")
    
    # Server Configuration
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", 8000))
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Environment
    environment: str = os.getenv("ENVIRONMENT", "development")
    
    # Redis Configuration
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # Swagger/OpenAPI Configuration
    enable_swagger: bool = os.getenv("ENABLE_SWAGGER", "True").lower() == "true"
    docs_url: str = "/docs" if os.getenv("ENABLE_SWAGGER", "True").lower() == "true" else None
    redoc_url: str = "/redoc" if os.getenv("ENABLE_SWAGGER", "True").lower() == "true" else None
    openapi_url: str = "/openapi.json" if os.getenv("ENABLE_SWAGGER", "True").lower() == "true" else None
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"


settings = Settings()
