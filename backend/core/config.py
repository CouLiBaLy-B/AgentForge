import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # API & General
    KANBAN_API_URL: str = os.getenv("KANBAN_API_URL", "http://localhost:3000")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost:5432/agentforge")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")

    # Tokens
    GITHUB_TOKEN: str = os.getenv("GITHUB_TOKEN", "")
    SLACK_BOT_TOKEN: str = os.getenv("SLACK_BOT_TOKEN", "")
    SLACK_SIGNING_SECRET: str = os.getenv("SLACK_SIGNING_SECRET", "")

    # LLM Infrastructure (vLLM / OpenAI)
    VLLM_BASE_URL: str = os.getenv("VLLM_BASE_URL", "http://localhost:8000/v1")
    
    # Model Configuration
    MAIN_MODEL: str = os.getenv("MAIN_MODEL", "openai:deepseek-v4")
    CODER_MODEL: str = os.getenv("CODER_MODEL", "openai:deepseek-v4")
    REVIEWER_MODEL: str = os.getenv("REVIEWER_MODEL", "openai:deepseek-v4")
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.1"))
    
    # Paths
    WORKSPACE_DIR: str = os.getenv("WORKSPACE_DIR", "./workspace")
    LOGS_DIR: str = os.getenv("LOGS_DIR", "./workspace/logs")
    MEMORY_DIR: str = os.getenv("MEMORY_DIR", "./backend/memory")
    SKILLS_DIR: str = os.getenv("SKILLS_DIR", "./skills")

    class Config:
        env_file = ".env"

settings = Settings()
