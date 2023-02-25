from fastapi import APIRouter, Depends, HTTPException, Response
from starlette import status

from app.api.dependencies.service import DependentService
from app.api.dependencies.user import get_current_user
from app.models.domain.user import User
from app.models.schemas.user import UserCredentials, UserIn, UserOut
from app.repositories.user import UserRepository
from app.services.user import UserService

router = APIRouter()


user_service = DependentService(UserService, UserRepository, is_security_settings=True)


@router.post('', response_model=UserOut, summary='Создание пользователя')
async def create_user(user: UserIn, service: UserService = Depends(user_service)):
    user = User(username=user.username, password=user.password)
    return await service.create_user(user)


@router.post('/authorization', response_model=UserCredentials, summary='Авторизация')
async def authorization_user(user: UserIn, service: UserService = Depends(user_service)):
    user = User(username=user.username, password=user.password)

    credentials = await service.authorization_user(user)
    if not credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='incorrect username or password')

    return credentials


@router.get('/me', response_model=UserOut, summary='Получить информация по JWT')
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user
