import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL_NAME: str = "gemini-1.5-flash"
    MONGO_URI: str = "mongodb://localhost:27017/privacy_auditor"
    SLACK_WEBHOOK_URL: str = "https://hooks.slack.com/services/MOCK/WEBHOOK"
    PORT: int = 8000
    HOST: str = "0.0.0.0"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Create a global settings instance
settings = Settings()
