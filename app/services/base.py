from typing import Type

from app.repositories.base import BaseRepository


class BaseService:
    def __init__(self, repository: Type[BaseRepository]) -> None:
        self.repository: Type[BaseRepository] = repository
