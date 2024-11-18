from fastapi import FastAPI
from contextlib import asynccontextmanager

from beanie import init_beanie

from backend.api.routes import router as main_router
from backend.db.database import client
from backend.models.beanie_models import __beanie_models__


def app_factory(lifespan):
    """Application Factory"""
    app = FastAPI(title="weather report", lifespan=lifespan)
    app.include_router(main_router)


    return app


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_beanie(database=client.db_name, document_models=__beanie_models__)
    yield  # This will keep the lifespan running
    # Cleanup code, if needed
    client.close()


app: FastAPI = app_factory(lifespan=lifespan)
