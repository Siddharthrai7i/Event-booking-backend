from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from app.core.config import settings

# Email connection config
conf = ConnectionConfig(
    MAIL_USERNAME   = settings.MAIL_USERNAME,
    MAIL_PASSWORD   = settings.MAIL_PASSWORD,
    MAIL_FROM       = settings.MAIL_FROM,
    MAIL_PORT       = settings.MAIL_PORT,
    MAIL_SERVER     = settings.MAIL_SERVER,
    MAIL_STARTTLS   = True,
    MAIL_SSL_TLS    = False,
    USE_CREDENTIALS = True,
)

async def send_otp_email(email: str, otp: str):
    message = MessageSchema(
        subject="Verify your Email — Event Booking System",
        recipients=[email],
        body=f"""
        <html>
            <body>
                <h2>Email Verification</h2>
                <p>Your OTP code is:</p>
                <h1 style="color: #3B82F6; letter-spacing: 8px;">{otp}</h1>
                <p>This code is valid for <b>5 minutes</b>.</p>
                <p>If you did not create an account, ignore this email.</p>
            </body>
        </html>
        """,
        subtype=MessageType.html
    )
    fm = FastMail(conf)
    await fm.send_message(message)