from app.core.settings.base import BaseAppSettings


class SecuritySettings(BaseAppSettings):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
