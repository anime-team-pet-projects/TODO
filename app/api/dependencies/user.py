from fastapi import Depends, HTTPException
from starlette import status

from app.api.dependencies.database import get_repository
from app.api.dependencies.security import get_security_settings
from app.core.settings.security import SecuritySettings
from app.models.domain.user import User
from app.pkg.security import JWTBearer, decode_access_token
from app.repositories.user import UserRepository


async def get_current_user(
    users: UserRepository = Depends(get_repository(UserRepository)),
    security_settings: SecuritySettings = Depends(get_security_settings),
    token: str = Depends(JWTBearer()),
) -> User:
    exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='credentials are not valid')

    payload = decode_access_token(token, security_settings.secret_key, security_settings.algorithm)
    if payload is None:
        raise exception

    username: str = payload.get('sub')
    if username is None:
        raise exception

    user = await users.get_by_username(username=username)
    if user is None:
        raise exception

    return user
