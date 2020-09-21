from di.repo.user import UserRedisRepoFactory
from usecase.interactor import PostForcastInteractor


class PostForcastInteractorFactory(object):
    @staticmethod
    async def get() -> PostForcastInteractor:
        await UserRedisRepoFactory.get()
        return PostForcastInteractor()
