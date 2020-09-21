from fastapi import APIRouter, Depends
from fastapi.responses import ORJSONResponse

from di import PostForcastInteractorFactory
from domain.entity import Forcast, Match, MatchResponse, ValidationErrorResponse, now
from usecase.interactor import PostForcastInteractor

router = APIRouter()


@router.post(
    "",
    response_class=ORJSONResponse,
    response_model=MatchResponse,
    responses={422: {"model": ValidationErrorResponse}},
    tags=["forcast"],
)
async def post_forcasts(
    body: Forcast,
    interactor: PostForcastInteractor = Depends(PostForcastInteractorFactory.get),
):
    match: Match = await interactor.execute(match_id=body.match_id, choice=body.choice)
    return {"servertime": now(), "content": match}
