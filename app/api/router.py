from fastapi import APIRouter

from app.api.routes import router as base_router
from app.api.v1.routes import router as v1_router

router = APIRouter()
router.include_router(base_router)
router.include_router(v1_router, prefix="/api/v1")
