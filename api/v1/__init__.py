from fastapi import APIRouter
from api.v1 import all

__all__ = ["router"]


router = APIRouter(prefix="/v1")
router.include_router(router=all.router)