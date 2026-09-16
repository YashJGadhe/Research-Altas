from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "ResearchAtlas"
    DEBUG: bool = False
    
    # MongoDB
    MONGODB_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "researchatlas_new"
    
    # JWT Configuration
    JWT_SECRET_KEY: str = "your-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    # Default Admin
    DEFAULT_ADMIN_EMAIL: str = "admin@raisoni.net"
    DEFAULT_ADMIN_PASSWORD: str = "Admin@123"
    
    # Email Domain Restrictions
    ADMIN_EMAIL_DOMAIN: str = "raisoni.net"
    FACULTY_EMAIL_DOMAIN: str = "raisoni.net"
    STUDENT_EMAIL_DOMAIN: str = "ghrce.raisoni.net"
    
    # ORCID
    ORCID_CLIENT_ID: str = ""
    ORCID_CLIENT_SECRET: str = ""
    
    # Scopus
    SCOPUS_API_KEY: str = ""
    
    # Web of Science
    WOS_API_KEY: str = ""
    
    # CORS
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"
    
    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
