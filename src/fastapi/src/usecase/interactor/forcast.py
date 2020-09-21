from domain.entity import Match


class ForcastBaseInteractor(object):
    pass


class PostForcastInteractor(ForcastBaseInteractor):
    async def execute(self, match_id: str, choice: int, *args, **kwargs) -> Match:
        match: Match = Match(match_id=match_id, pitcher="金田正一", batter="王貞治")
        match.choices[choice] += 1
        return match
