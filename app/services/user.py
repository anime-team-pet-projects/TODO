from typing import Optional

from app.core.settings.security import SecuritySettings
from app.models.domain.user import User
from app.models.schemas.user import UserCredentials
from app.pkg.security import create_access_token, hash_password, verify_password
from app.repositories.user import UserRepository
from app.services.base import BaseService


class UserService(BaseService):
    def __init__(self, repository: UserRepository, security_settings: SecuritySettings) -> None:
        self.repository = repository
        self.security_settings = security_settings

    async def create_user(self, user: User) -> User:
        user.password = hash_password(user.password)
        return await self.repository.create(user)

    async def authorization_user(self, login_user: User) -> Optional[UserCredentials]:
        user = await self.repository.get_by_username(login_user.username)

        if user is None or not verify_password(login_user.password, user.password):
            return

        return UserCredentials(
            access=create_access_token({"sub": user.username}, **self.security_settings.dict()),
        )
