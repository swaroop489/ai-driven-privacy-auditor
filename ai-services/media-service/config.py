from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    NLP_SERVICE_URL: str = "http://localhost:8000/api/v1/predict"
    PORT: int = 8003
    HOST: str = "0.0.0.0"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Create a global settings instance
settings = Settings()
