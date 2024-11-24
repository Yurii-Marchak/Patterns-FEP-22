from fastapi import APIRouter
from backend.api.routes.sports import sports_router

router = APIRouter()
router.include_router(sports_router, prefix="/sports", tags=["sports"])
