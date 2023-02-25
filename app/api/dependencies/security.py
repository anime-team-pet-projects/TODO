from starlette.requests import Request

from app.core.settings.security import SecuritySettings


def get_security_settings(request: Request) -> SecuritySettings:
    return request.app.state.security_settings
