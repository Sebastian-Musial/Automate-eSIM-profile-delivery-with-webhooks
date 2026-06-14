from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str = Field(validation_alias="DATABASE_URL")
    app_title: str = "Automatyzacja dostawy profili eSIM"
    app_description: str = ("Projekt FastAPI do automatyzacji wysyłki profili eSIM")
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    webhook_token: str = Field(validation_alias="PAYMENT_WEBHOOK_TOKEN")


def get_settings() -> Settings:
    return Settings()