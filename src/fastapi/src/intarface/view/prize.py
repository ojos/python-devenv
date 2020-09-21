from fastapi import APIRouter, Depends
from fastapi.responses import ORJSONResponse

from di import GetPrizeInteractorFactory
from domain.entity import Prize, PrizeResponse, ValidationErrorResponse, now
from usecase.interactor import GetPrizeInteractor

router = APIRouter()


@router.get(
    "/{user_id}",
    response_class=ORJSONResponse,
    response_model=PrizeResponse,
    responses={422: {"model": ValidationErrorResponse}},
    tags=["prize"],
)
async def get_prizes(
    user_id: str,
    interactor: GetPrizeInteractor = Depends(GetPrizeInteractorFactory.get),
):
    prize: Prize = await interactor.execute(user_id=user_id)
    return {"servertime": now(), "content": prize}
