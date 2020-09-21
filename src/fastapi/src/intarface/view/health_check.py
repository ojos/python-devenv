from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

router = APIRouter()


@router.get("", response_class=PlainTextResponse, tags=["health_check"])
async def health_check():
    return "OK"
