import pyotp

OTP_EXPIRY_SECONDS = 300  # 5 minutes

def generate_otp() -> tuple[str, str]:
    # Generate a random secret and OTP
    secret = pyotp.random_base32()
    totp   = pyotp.TOTP(secret, interval=OTP_EXPIRY_SECONDS)
    otp    = totp.now()
    return otp, secret

def verify_otp(otp: str, secret: str) -> bool:
    totp = pyotp.TOTP(secret, interval=OTP_EXPIRY_SECONDS)
    return totp.verify(otp, valid_window=1)