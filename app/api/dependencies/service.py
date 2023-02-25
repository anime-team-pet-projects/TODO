from typing import Type

from databases import Database
from fastapi import Depends

from app.api.dependencies.database import _get_db_pool
from app.api.dependencies.security import get_security_settings
from app.core.settings.security import SecuritySettings
from app.repositories.base import BaseRepository
from app.services.base import BaseService


class DependentService:
    def __init__(
        self, service: Type[BaseService], repository: Type[BaseRepository], is_security_settings: bool = False
    ) -> None:
        self.repository = repository
        self.service = service
        self.is_security_settings = is_security_settings

    # TODO: review
    def __call__(
        self,
        database: Database = Depends(_get_db_pool),
        security_settings: SecuritySettings = Depends(get_security_settings),
    ) -> BaseService:
        if not self.is_security_settings:
            return self.service(self.repository(database))
        return self.service(self.repository(database), security_settings)
