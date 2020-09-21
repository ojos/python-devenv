from di.repo.user import UserRedisRepoFactory
from usecase.interactor import GetPrizeInteractor


class GetPrizeInteractorFactory(object):
    @staticmethod
    async def get() -> GetPrizeInteractor:
        await UserRedisRepoFactory.get()
        return GetPrizeInteractor()
