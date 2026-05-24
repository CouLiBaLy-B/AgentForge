from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # API & General
    KANBAN_API_URL: str = os.getenv("KANBAN_API_URL", "http://localhost:3000")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost:5432/agentforge")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")

    # Tokens
    GITHUB_TOKEN: str = os.getenv("GITHUB_TOKEN", "")
    SLACK_BOT_TOKEN: str = os.getenv("SLACK_BOT_TOKEN", "")
    SLACK_SIGNING_SECRET: str = os.getenv("SLACK_SIGNING_SECRET", "")

    # LLM Infrastructure
    LLM_SOURCE: str = os.getenv("LLM_SOURCE", "vllm")
    VLLM_BASE_URL: str = os.getenv("VLLM_BASE_URL", "http://vllm:8000/v1")
    FREELLM_BASE_URL: str = os.getenv("FREELLM_BASE_URL", "http://freellm:3001/v1")
    FREELLM_API_KEY: str = os.getenv("FREELLM_API_KEY", "")
    
    # Claude Code Specific
    CLAUDE_CODE_ENABLED: bool = os.getenv("CLAUDE_CODE_ENABLED", "true").lower() == "true"
    CLAUDE_CODE_MODEL_MAPPING: str = os.getenv("CLAUDE_CODE_MODEL_MAPPING", "qwen-2.5-coder-32b")
    
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

settings = Settings()
