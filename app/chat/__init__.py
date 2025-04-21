from fastapi import APIRouter
from .websockets import router as chat_router

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
)
router.include_router(chat_router)
