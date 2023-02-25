import datetime
from fastapi import Request, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from jose import jwt

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hash: str) -> bool:
    return pwd_context.verify(password, hash)


def create_access_token(data: dict, secret_key: str, algorithm: str, access_token_expire_minutes: int) -> str:
    to_encode = data.copy()
    to_encode.update({'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=access_token_expire_minutes)})
    return jwt.encode(to_encode, secret_key, algorithm=algorithm)


def decode_access_token(token: str, secret_key: str, algorithm: str):
    try:
        encoded_jwt = jwt.decode(token, secret_key, algorithms=[algorithm])
    except jwt.JWSError:
        return None
    return encoded_jwt


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)

        exp = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='invalid auth token')

        if credentials:
            token = decode_access_token(
                credentials.credentials,
                request.app.state.security_settings.secret_key,
                request.app.state.security_settings.algorithm,
            )
            if token is None:
                raise exp
            return credentials.credentials
        else:
            raise exp
