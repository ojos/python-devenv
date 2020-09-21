from fastapi import APIRouter

from intarface.view import forcast, health_check, prize, user

router = APIRouter()

router.include_router(forcast.router, prefix="/api/forcasts", tags=["forcast"])
router.include_router(prize.router, prefix="/api/prizes", tags=["prize"])
router.include_router(user.router, prefix="/api/users", tags=["user"])
router.include_router(
    health_check.router, prefix="/health_check", tags=["health_check"]
)
