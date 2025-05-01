"""Settings and env vars."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    """Database Settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        env_prefix="DB_",
    )

    db_url: str = "sqlite:///./glucose.db"
    sql_echo_pool: str = "debug"


class Settings(BaseSettings):
    """Settings class."""

    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore", env_prefix="GLUC_"
    )

    api_key_name: str = "apikey"
    api_keys: list[str]


settings = Settings()  # type: ignore
db_settings = DatabaseSettings()  # type: ignore
