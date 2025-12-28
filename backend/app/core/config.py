from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GROQ_API_KEY: str = "your_groq_api_key"
    PIXABAY_API_KEY: str = ""
    REDIS_URL: str = "redis://localhost:6379/0"
    DATABASE_URL: str = "sqlite:///./video_generator.db"
    STORAGE_TYPE: str = "local"
    STORAGE_PATH: str = "./videos"
    FRONTEND_URL: str = "http://localhost:5173"
    DEBUG: bool = True

    class Config:
        env_file = ".env"

settings = Settings()
