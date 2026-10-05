from typing import List, Union
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator

class Settings(BaseSettings):
    PROJECT_NAME: str = "CoA Directory Extractor"
    VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api"
    
    # Target Council of Architecture Portal
    COA_BASE_URL: str = "https://www.coa.gov.in"
    
    # Database
    DATABASE_URL: str = "sqlite:///./coa_directory.db"
    
    # Performance & Concurrency Limits (Safe free-tier defaults)
    MAX_CONCURRENCY: int = 5
    REQUESTS_PER_SECOND: float = 2.0
    REQUEST_TIMEOUT: int = 30
    MAX_RETRIES: int = 3
    BATCH_SIZE: int = 50
    
    # Operational Mode
    USE_MOCK_DATA: bool = False
    
    # CORS
    CORS_ORIGINS: Union[str, List[str]] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ]
    
    @field_validator("CORS_ORIGINS", mode="before")
    def parse_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",") if i.strip()]
        elif isinstance(v, list):
            return v
        return ["*"]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

settings = Settings()
