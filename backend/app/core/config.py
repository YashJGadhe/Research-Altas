"""
ResearchAtlas - Application Configuration

Centralized configuration loaded from environment variables.
Never hardcode secrets - always use environment variables.
"""

import os
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    APP_NAME: str = "ResearchAtlas"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # MongoDB
    MONGODB_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "researchatlas"

    # JWT Configuration
    JWT_SECRET_KEY: str = "change-this-in-production-use-strong-random-secret"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Default Admin
    DEFAULT_ADMIN_EMAIL: str = "admin@raisoni.net"
    DEFAULT_ADMIN_PASSWORD: str = "Admin@123"

    # CORS
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"

    # Email Domain Restrictions
    ADMIN_EMAIL_DOMAIN: str = "raisoni.net"
    FACULTY_EMAIL_DOMAIN: str = "raisoni.net"
    STUDENT_EMAIL_DOMAIN: str = "ghrce.raisoni.net"

    @property
    def cors_origins_list(self) -> list:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

    @property
    def role_email_domains(self) -> dict:
        """Get email domain restrictions per role."""
        return {
            "admin": self.ADMIN_EMAIL_DOMAIN,
            "faculty": self.FACULTY_EMAIL_DOMAIN,
            "student": self.STUDENT_EMAIL_DOMAIN,
        }

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Singleton settings instance
settings = Settings()
