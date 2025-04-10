from fastapi import APIRouter

from app.core.config import settings
from .companies import router as company_router
from .users import router as users_router
from app.api.jwt import router as demo_jwt_auth_router


router = APIRouter(
    prefix=settings.api.prefix,
)

router.include_router(
    company_router,
)
router.include_router(
    users_router,
)

router.include_router(
    demo_jwt_auth_router,
)
