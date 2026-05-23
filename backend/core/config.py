import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    VLLM_BASE_URL: str = os.getenv("VLLM_BASE_URL", "http://localhost:8000/v1")
    GITHUB_TOKEN: str = os.getenv("GITHUB_TOKEN", "")
    SLACK_BOT_TOKEN: str = os.getenv("SLACK_BOT_TOKEN", "")
    SLACK_SIGNING_SECRET: str = os.getenv("SLACK_SIGNING_SECRET", "")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost:5432/agentforge")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    KANBAN_API_URL: str = os.getenv("KANBAN_API_URL", "http://localhost:3000")

    class Config:
        env_file = ".env"

settings = Settings()
