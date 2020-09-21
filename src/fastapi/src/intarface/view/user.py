from fastapi import APIRouter, Depends
from fastapi.responses import ORJSONResponse

from di import CreateUserInteractorFactory, GetUserInteractorFactory
from domain.entity import User, UserResponse, ValidationErrorResponse, now
from usecase.interactor import CreateUserInteractor, GetUserInteractor

router = APIRouter()


@router.post(
    "",
    response_class=ORJSONResponse,
    response_model=UserResponse,
    responses={422: {"model": ValidationErrorResponse}},
    tags=["user"],
)
async def post_users(
    body: User,
    interactor: CreateUserInteractor = Depends(CreateUserInteractorFactory.get),
):
    user = await interactor.execute(
        name=body.name, icon_id=body.icon_id, number=body.number
    )
    return {"servertime": now(), "content": user}


@router.get(
    "/{user_id}",
    response_class=ORJSONResponse,
    response_model=UserResponse,
    responses={422: {"model": ValidationErrorResponse}},
    tags=["user"],
)
async def get_users(
    user_id: str,
    interactor: GetUserInteractor = Depends(GetUserInteractorFactory.get),
):
    user = await interactor.execute(user_id=user_id)
    return {"servertime": now(), "content": user}
