from fastapi import APIRouter

from app.core.config import settings
from .companies import router as company_router
from .users import router as users_router

router = APIRouter(
    prefix=settings.api.prefix,
)

router.include_router(
    company_router,
)
router.include_router(
    users_router,
)
