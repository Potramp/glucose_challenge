"""Config for glucose app."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """General Settings."""

    env_name: str = "Local"
    base_url: str = "http://localhost:8000"
    db_url: str = "sqlite:///./glucose.db"


def get_settings() -> Settings:
    """Get settings."""
    settings = Settings()
    print(f"Loading settings for: {settings.env_name}")
    return settings
