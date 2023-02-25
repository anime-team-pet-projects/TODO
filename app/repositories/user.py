from sqlalchemy import insert, select

from app.models.domain.user import User
from app.db.models.user import User as UserModel
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository):
    async def create(self, user: User) -> User:
        query = insert(UserModel).values(**user.dict(exclude={'id'}))

        user.id = await self.database.execute(query)
        return user

    async def get_by_username(self, username: str) -> User:
        query = select(UserModel).where(UserModel.username == username)

        user: UserModel = await self.database.fetch_one(query)

        return self.model_to_domain(user)

    @classmethod
    def model_to_domain(cls, model: UserModel) -> User:
        return User(
            id=model.id,
            username=model.username,
            password=model.password,
        )
