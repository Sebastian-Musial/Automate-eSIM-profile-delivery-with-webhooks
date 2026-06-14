from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.database import create_db_and_tables
from app.routers.webhook import router

def create_app(create_tables_on_startup: bool = True) -> FastAPI:
    application = FastAPI()

    @application.get("/health", tags=["system"])
    def health_check() -> dict[str, str]:
        return {"status": "ok"}

    if create_tables_on_startup:
        create_db_and_tables()

    application.include_router(router)
    application.mount("/static", StaticFiles(directory="static"), name="static")

    return application

app = create_app()