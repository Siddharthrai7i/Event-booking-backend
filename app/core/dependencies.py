from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.security import decode_token
from app.repositories.user_repo import get_user_by_id
from app.models.user import User
from app.utils.exceptions import (
    InvalidTokenException,
    UnauthorizedException,
    EmailNotVerifiedException
)

# This reads the token from the Authorize button automatically
security = HTTPBearer()


def get_current_user(
    credentials : HTTPAuthorizationCredentials = Depends(security),
    db          : Session = Depends(get_db)
) -> User:
    token   = credentials.credentials
    payload = decode_token(token)

    if not payload or payload.get("type") != "access":
        raise InvalidTokenException()

    user = get_user_by_id(db, payload["sub"])
    if not user:
        raise InvalidTokenException()

    return user


def get_verified_user(
    current_user: User = Depends(get_current_user)
) -> User:
    if not current_user.is_verified:
        raise EmailNotVerifiedException()
    return current_user


def get_admin_user(
    current_user: User = Depends(get_verified_user)
) -> User:
    if current_user.role != "admin":
        raise UnauthorizedException()
    return current_user