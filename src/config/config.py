from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseSettings):
    CLAUDE_API_KEY: str = os.getenv("CLAUDE_API_KEY", "")
    DB_HOST: str = os.getenv("POSTGRES_HOST", "")
    DB_PORT: int = int(os.getenv("POSTGRES_PORT", 5432))
    DB_USER: str = os.getenv("POSTGRES_USER", "")
    DB_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "")
    DB_NAME: str = os.getenv("POSTGRES_DB", "")
    DB_URL: str = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(self.DB_URL)


settings = Settings()
