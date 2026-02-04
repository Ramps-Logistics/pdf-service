from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_KEY: str | None = None
    MAX_BROWSER_CONTEXTS: int = 4
    PORT: int = 8000

    class Config:
        env_file = ".env"


settings = Settings()
