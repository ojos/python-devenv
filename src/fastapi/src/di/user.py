from di.repo.user import UserRedisRepoFactory
from usecase.interactor import CreateUserInteractor, GetUserInteractor


class CreateUserInteractorFactory(object):
    @staticmethod
    async def get() -> CreateUserInteractor:
        await UserRedisRepoFactory.get()
        return CreateUserInteractor()


class GetUserInteractorFactory(object):
    @staticmethod
    async def get() -> GetUserInteractor:
        await UserRedisRepoFactory.get()
        return GetUserInteractor()
