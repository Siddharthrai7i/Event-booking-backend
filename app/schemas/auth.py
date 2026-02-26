from pydantic import BaseModel, EmailStr
from uuid import UUID

class LoginRequest(BaseModel):
    email:    EmailStr
    password: str

class SignupRequest(BaseModel):
    email:    EmailStr
    password: str

class RefreshRequest(BaseModel):
    refresh_token: str

# OTP schemas
class SendOTPRequest(BaseModel):
    email: EmailStr

class VerifyOTPRequest(BaseModel):
    email: EmailStr
    otp:   str

class TokenResponse(BaseModel):
    access_token:  str
    refresh_token: str
    token_type:    str = "bearer"

class UserOut(BaseModel):
    id:          UUID
    email:       str
    role:        str
    is_verified: bool

    class Config:
        from_attributes = True