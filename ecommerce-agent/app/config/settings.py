"""应用配置"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """应用配置类"""

    # ---- LLM 配置 ----
    deepseek_api_key: str = ""
    deepseek_base_url: str = "https://api.deepseek.com/v1"
    deepseek_model: str = "deepseek-chat"

    dashscope_api_key: str = ""
    qwen_model: str = "qwen-plus"

    # ---- PostgreSQL ----
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_user: str = "medical"
    postgres_password: str = "medical123"
    postgres_db: str = "ecommerce_agent"

    @property
    def postgres_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def postgres_url_sync(self) -> str:
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    # ---- Redis ----
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0

    @property
    def redis_url(self) -> str:
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"

    # ---- Milvus ----
    milvus_host: str = "localhost"
    milvus_port: int = 19530

    # ---- Embedding（阿里百炼）----
    embedding_model: str = "text-embedding-v3"
    embedding_dim: int = 1024

    # ---- LangSmith ----
    langchain_tracing_v2: bool = True
    langchain_api_key: str = ""
    langchain_project: str = "ecommerce-agent"

    # ---- 应用配置 ----
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    app_env: str = "development"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
