from domain.entity import Prize


class PrizeBaseInteractor(object):
    pass


class GetPrizeInteractor(PrizeBaseInteractor):
    async def execute(self, user_id: str, *args, **kwargs) -> Prize:
        prize: Prize = Prize(
            keyword="おうさん",
            url="https://www.ntv.co.jp/baseball/articles/34tzny3lhgoowrp0fn.html",
        )
        return prize
