from domain.entity import User


class UserBaseInteractor(object):
    pass


class CreateUserInteractor(UserBaseInteractor):
    async def execute(
        self, name: str, icon_id: str, number: str, *args, **kwargs
    ) -> User:
        user: User = User(name=name, icon_id=icon_id, number=number)
        return user


class GetUserInteractor(UserBaseInteractor):
    async def execute(self, user_id: str, *args, **kwargs) -> User:
        user: User = User(
            user_id=user_id,
            name="アリス",
            icon_id="00002",
            number="001",
            inning_point=0,
            total_point=0,
        )
        return user
