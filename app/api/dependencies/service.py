from typing import Type

from databases import Database
from fastapi import Depends

from app.api.dependencies.database import _get_db_pool
from app.repositories.base import BaseRepository
from app.services.base import BaseService


class DependentService:
    def __init__(self, service: Type[BaseService], repository: Type[BaseRepository]) -> None:
        self.repository = repository
        self.service = service

    def __call__(self, database: Database = Depends(_get_db_pool)) -> BaseService:
        return self.service(self.repository(database))
