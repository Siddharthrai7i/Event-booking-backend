from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.auth import (
    LoginRequest, SignupRequest, RefreshRequest,
    TokenResponse, UserOut, SendOTPRequest, VerifyOTPRequest
)
from app.services.auth_service import (
    login_user, signup_user, refresh_access_token,
    send_verification_otp, verify_email_otp
)
from app.core.dependencies import get_current_user, get_verified_user
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Auth"])

# ── Public routes (no auth needed) ───────────────
@router.post("/signup", response_model=TokenResponse, status_code=201)
def signup(payload: SignupRequest, db: Session = Depends(get_db)):
    return signup_user(db, payload.email, payload.password)

@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    return login_user(db, payload.email, payload.password)

@router.post("/refresh", response_model=TokenResponse)
def refresh(payload: RefreshRequest):
    return refresh_access_token(payload.refresh_token)

@router.post("/send-otp")
async def send_otp(payload: SendOTPRequest, db: Session = Depends(get_db)):
    return await send_verification_otp(db, payload.email)

@router.post("/verify-otp")
async def verify_otp_route(payload: VerifyOTPRequest, db: Session = Depends(get_db)):
    return await verify_email_otp(db, payload.email, payload.otp)

# ── Protected routes (verified users only) ────────
@router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_verified_user)):
    return current_user