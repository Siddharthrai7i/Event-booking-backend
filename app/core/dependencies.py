from fastapi import Depends, Header
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


def get_current_user(
    authorization: str = Header(...),
    db: Session = Depends(get_db)
) -> User:
    # Extract token from "Bearer <token>"
    if not authorization.startswith("Bearer "):
        raise InvalidTokenException()

    token   = authorization.split(" ")[1]
    payload = decode_token(token)

    if not payload or payload.get("type") != "access":
        raise InvalidTokenException()

    # Fetch user from DB
    user = get_user_by_id(db, payload["sub"])
    if not user:
        raise InvalidTokenException()

    return user


def get_verified_user(
    current_user: User = Depends(get_current_user)
) -> User:
    # Block access if email not verified
    if not current_user.is_verified:
        raise EmailNotVerifiedException()
    return current_user


def get_admin_user(
    current_user: User = Depends(get_verified_user)
) -> User:
    if current_user.role != "admin":
        raise UnauthorizedException()
    return current_user