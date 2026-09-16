from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # MongoDB
    MONGODB_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "researchatlas_new"
    
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
