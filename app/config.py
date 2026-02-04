from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    max_browser_contexts: int = 4
    render_timeout_ms: int = 30000
    max_html_size_bytes: int = 5_000_000
    api_key: str | None = None

    class Config:
        env_file = ".env"

settings = Settings()
