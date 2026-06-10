from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str = Field(validation_alias="DATABASE_URL")
    app_title: str = "Automatyzacja dostawy profilie eSIM"
    app_description: str = ("Projekt FastAPI do automatyzacji wysyłki profili eSIM")
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


def get_settings() -> Settings:
    return Settings()