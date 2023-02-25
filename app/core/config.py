from app.core.settings.app import AppSettings
from app.core.settings.security import SecuritySettings


def get_app_settings() -> AppSettings:
    return AppSettings()


def get_security_settings(secret_key: str, algorithm: str, access_token_expire_minutes: int):
    return SecuritySettings(
        secret_key=secret_key,
        algorithm=algorithm,
        access_token_expire_minutes=access_token_expire_minutes,
    )
