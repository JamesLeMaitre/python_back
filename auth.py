from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi_auth import AuthError, BaseAuth

from .models import User
from .database import get_db_session


class JWTAuth(BaseAuth):
    auth_error = HTTPException(status_code=401, detail="Unauthorized")

    async def get_user(self, token: str) -> User:
        try:
            session = next(get_db_session())
            user = await session.query(User).filter_by(token=token).first()
            if user is None:
                raise AuthError()
            return user
        except:
            raise AuthError()

    async def authenticate(self, credentials: HTTPAuthorizationCredentials) -> User:
        try:
            token = credentials.credentials
            user = await self.get_user(token)
            return user
        except:
            raise AuthError()


http_bearer = HTTPBearer()
jwt_auth = JWTAuth()


async def get_current_user(token: str = Depends(http_bearer)) -> User:
    user = await jwt_auth(credentials=token)
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_current_active_admin(current_user: User = Depends(get_current_active_user)) -> User:
    if not current_user.is_admin:
        raise HTTPException(status_code=400, detail="Non-admin user")
    return current_user
