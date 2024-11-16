from fastapi import FastAPI
from contextlib import asynccontextmanager
from beanie import init_beanie
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from backend.api.routes import router as main_router
from backend.db.database import client
from backend.models.sports_models import __beanie_models__


def app_factory(lifespan):
    """Application Factory"""
    app = FastAPI(title="sports report", lifespan=lifespan)
    app.include_router(main_router)
    return app

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_beanie(database=client.db_name, document_models=__beanie_models__)
    yield  
    client.close()


app = app_factory(lifespan=lifespan)

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("frontend/index.html") as f:
        return f.read()
    
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")