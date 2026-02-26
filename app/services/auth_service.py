from sqlalchemy.orm import Session
from app.repositories.user_repo import (
    get_user_by_email,
    create_user,
    mark_user_verified,
)
from app.core.security import (
    verify_password,
    hash_password,
    create_access_token,
    create_refresh_token,
    decode_token
)
from app.schemas.auth import TokenResponse
from app.utils.exceptions import (
    InvalidCredentialsException,
    InvalidTokenException,
    EmailAlreadyExistsException,
    InvalidOTPException,
    EmailNotRegisteredException,
    AlreadyVerifiedException
)
from app.utils.otp import generate_otp, verify_otp
from app.utils.email import send_otp_email
from app.db.redis import redis_client

# Redis key pattern
OTP_KEY = "otp:secret:{email}"   # e.g. otp:secret:john@example.com
OTP_EXPIRY = 300                  # 5 minutes


def signup_user(db: Session, email: str, password: str) -> TokenResponse:
    existing_user = get_user_by_email(db, email)
    if existing_user:
        raise EmailAlreadyExistsException()

    password_hash = hash_password(password)
    user          = create_user(db, email=email, password_hash=password_hash)
    token_data    = {"sub": str(user.id), "email": user.email, "role": user.role}
    access_token  = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


def login_user(db: Session, email: str, password: str) -> TokenResponse:
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.password_hash):
        raise InvalidCredentialsException()

    token_data    = {"sub": str(user.id), "email": user.email, "role": user.role}
    access_token  = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


def refresh_access_token(refresh_token: str) -> TokenResponse:
    payload = decode_token(refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise InvalidTokenException()

    token_data        = {"sub": payload["sub"], "email": payload["email"], "role": payload["role"]}
    new_access_token  = create_access_token(token_data)
    new_refresh_token = create_refresh_token(token_data)

    return TokenResponse(access_token=new_access_token, refresh_token=new_refresh_token)


async def send_verification_otp(db: Session, email: str):
    # Step 1: Check user exists
    user = get_user_by_email(db, email)
    if not user:
        raise EmailNotRegisteredException()

    # Step 2: Check not already verified
    if user.is_verified:
        raise AlreadyVerifiedException()

    # Step 3: Generate OTP + secret
    otp, secret = generate_otp()

    # Step 4: Store secret in Redis with 5 min expiry
    # ✅ No DB write — auto deleted after 5 minutes
    key = OTP_KEY.format(email=email)
    await redis_client.setex(key, OTP_EXPIRY, secret)

    # Step 5: Send OTP to email
    await send_otp_email(email, otp)

    return {"message": f"OTP sent to {email}. Valid for 5 minutes."}


async def verify_email_otp(db: Session, email: str, otp: str):
    # Step 1: Fetch user
    user = get_user_by_email(db, email)
    if not user:
        raise EmailNotRegisteredException()

    # Step 2: Check not already verified
    if user.is_verified:
        raise AlreadyVerifiedException()

    # Step 3: Fetch secret from Redis
    key    = OTP_KEY.format(email=email)
    secret = await redis_client.get(key)

    # Step 4: Check secret exists (not expired)
    if not secret:
        raise InvalidOTPException()  # OTP expired or never sent

    # Step 5: Verify OTP
    if not verify_otp(otp, secret):
        raise InvalidOTPException()  # Wrong OTP

    # Step 6: Mark user verified in DB
    mark_user_verified(db, user)

    # Step 7: Delete OTP secret from Redis immediately
    await redis_client.delete(key)

    return {"message": "Email verified successfully ✅"}