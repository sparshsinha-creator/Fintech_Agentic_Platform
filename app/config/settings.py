"""Application configuration management using pydantic-settings."""

from __future__ import annotations

import os
from pathlib import Path
from typing import ClassVar

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    APP_NAME: str = "MyFinance"
    APP_VERSION: str = "0.1.0"
    APP_ENV: str = "development"
    APP_DEBUG: bool = True
    APP_SECRET_KEY: str = "change-me-to-a-random-secret"
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000

    # JWT
    JWT_SECRET_KEY: str = "change-me-to-a-random-secret"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Database
    DATABASE_URL: str = "mysql+mysqlconnector://user:password@localhost:3306/myfinance_db"
    DATABASE_ECHO: bool = False
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20
    DATABASE_POOL_PRE_PING: bool = True

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_CACHE_TTL: int = 300

    # Google Gemini
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-2.5-flash-latest"
    GEMINI_TEMPERATURE: float = 0.3
    GEMINI_MAX_RETRIES: int = 3

    # LangChain
    LANGCHAIN_TRACING_V2: bool = False
    LANGCHAIN_API_KEY: str = ""
    LANGCHAIN_PROJECT: str = "myfinance"

    # FAISS
    FAISS_INDEX_PATH: str = "data/embeddings/faiss_index.bin"
    FAISS_EMBEDDING_DIMENSION: int = 768
    FAISS_SIMILARITY_METRIC: str = "cosine"

    # RAG
    RAG_CHUNK_SIZE: int = 1000
    RAG_CHUNK_OVERLAP: int = 200
    RAG_TOP_K: int = 5
    RAG_MIN_SIMILARITY: float = 0.7

    # File Upload
    UPLOAD_MAX_SIZE_MB: int = 10
    UPLOAD_ALLOWED_EXTENSIONS: str = ".pdf,.csv,.xlsx,.docx,.txt"

    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW_SECONDS: int = 60

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"
    LOG_FILE_PATH: str = "logs/myfinance.log"

    @property
    def database_url(self) -> str:
        return self.DATABASE_URL

    @property
    def redis_url(self) -> str:
        return self.REDIS_URL

    @property
    def gemini_api_key(self) -> str:
        return self.GEMINI_API_KEY

    @property
    def is_development(self) -> bool:
        return self.APP_ENV.lower() == "development"

    @property
    def allowed_extensions_list(self) -> list[str]:
        return [ext.strip() for ext in self.UPLOAD_ALLOWED_EXTENSIONS.split(",")]

    @property
    def log_file_path(self) -> Path:
        path = Path(self.LOG_FILE_PATH)
        os.makedirs(path.parent, exist_ok=True)
        return path


settings = Settings()  # type: ignore[call-arg]
