"""
core/config.py

App settings, loaded from environment variables (or a .env file).
See .env.example for the variables this expects.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Path to the exported pipeline, relative to the backend/ folder
    model_path: str = "models/house_price.pkl"

    # Comma-separated list of allowed frontend origins for CORS
    cors_origins: str = "http://localhost:5173"

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


settings = Settings()
