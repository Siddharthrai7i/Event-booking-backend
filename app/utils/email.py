from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from app.core.config import settings

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
        subject    = "Verify your Email — Event Booking System",
        recipients = [email],
        body       = f"""
        <html>
            <body style="font-family: Arial, sans-serif; padding: 20px;">
                <h2>Email Verification</h2>
                <p>Your OTP code is:</p>
                <h1 style="color: #3B82F6; letter-spacing: 8px;">{otp}</h1>
                <p>This code is valid for <b>5 minutes</b>.</p>
                <p>If you did not create an account, ignore this email.</p>
            </body>
        </html>
        """,
        subtype = MessageType.html
    )
    fm = FastMail(conf)
    await fm.send_message(message)


async def send_booking_confirmation_email(
    email      : str,
    user_name  : str,
    event_name : str,
    event_city : str,
    event_venue: str,
    event_date : str,
    seat_number: str,
    category   : str,
    amount     : float,
    booking_id : str,
    payment_id : str,
    paid_on    : str,
):
    message = MessageSchema(
        subject    = f"Booking Confirmed 🎉 — {event_name}",
        recipients = [email],
        body       = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 30px;">
            <div style="max-width: 600px; margin: auto; background: white; 
                        border-radius: 10px; padding: 30px; 
                        box-shadow: 0 2px 10px rgba(0,0,0,0.1);">

                <!-- Header -->
                <div style="text-align: center; background-color: #10B981; 
                            padding: 20px; border-radius: 8px; margin-bottom: 30px;">
                    <h1 style="color: white; margin: 0;">✅ Booking Confirmed!</h1>
                </div>

                <!-- Greeting -->
                <p style="font-size: 16px;">Hi <b>{user_name}</b>,</p>
                <p style="font-size: 16px; color: #555;">
                    Your booking has been confirmed. Here are your details:
                </p>

                <!-- Event Details -->
                <div style="background: #F0FDF4; border-left: 4px solid #10B981; 
                            padding: 15px; margin: 20px 0; border-radius: 4px;">
                    <h3 style="color: #10B981; margin-top: 0;">🎭 Event Details</h3>
                    <table style="width: 100%; border-collapse: collapse;">
                        <tr>
                            <td style="padding: 8px 0; color: #666; width: 35%;">Event</td>
                            <td style="padding: 8px 0;"><b>{event_name}</b></td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0; color: #666;">Venue</td>
                            <td style="padding: 8px 0;"><b>{event_venue}</b></td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0; color: #666;">City</td>
                            <td style="padding: 8px 0;"><b>{event_city}</b></td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0; color: #666;">Date & Time</td>
                            <td style="padding: 8px 0;"><b>{event_date}</b></td>
                        </tr>
                    </table>
                </div>

                <!-- Seat Details -->
                <div style="background: #EFF6FF; border-left: 4px solid #3B82F6;
                            padding: 15px; margin: 20px 0; border-radius: 4px;">
                    <h3 style="color: #3B82F6; margin-top: 0;">💺 Seat Details</h3>
                    <table style="width: 100%; border-collapse: collapse;">
                        <tr>
                            <td style="padding: 8px 0; color: #666; width: 35%;">Seat Number</td>
                            <td style="padding: 8px 0;"><b>{seat_number}</b></td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0; color: #666;">Category</td>
                            <td style="padding: 8px 0;">
                                <span style="background: #3B82F6; color: white; 
                                            padding: 2px 10px; border-radius: 20px; 
                                            font-size: 13px;">
                                    {category}
                                </span>
                            </td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0; color: #666;">Amount Paid</td>
                            <td style="padding: 8px 0;">
                                <b style="color: #10B981; font-size: 18px;">₹{amount:,.2f}</b>
                            </td>
                        </tr>
                    </table>
                </div>

                <!-- Booking Details -->
                <div style="background: #FFF7ED; border-left: 4px solid #F59E0B;
                            padding: 15px; margin: 20px 0; border-radius: 4px;">
                    <h3 style="color: #F59E0B; margin-top: 0;">📋 Booking Details</h3>
                    <table style="width: 100%; border-collapse: collapse;">
                        <tr>
                            <td style="padding: 8px 0; color: #666; width: 35%;">Booking ID</td>
                            <td style="padding: 8px 0; font-size: 13px; 
                                       font-family: monospace;">{booking_id}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0; color: #666;">Payment ID</td>
                            <td style="padding: 8px 0; font-size: 13px;
                                       font-family: monospace;">{payment_id}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0; color: #666;">Status</td>
                            <td style="padding: 8px 0;">
                                <span style="background: #10B981; color: white;
                                            padding: 2px 10px; border-radius: 20px;
                                            font-size: 13px;">
                                    CONFIRMED ✅
                                </span>
                            </td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0; color: #666;">Paid On</td>
                            <td style="padding: 8px 0;"><b>{paid_on}</b></td>
                        </tr>
                    </table>
                </div>

                <!-- Footer -->
                <div style="text-align: center; margin-top: 30px; 
                            padding-top: 20px; border-top: 1px solid #eee;">
                    <p style="color: #888; font-size: 14px;">
                        Thank you for booking with <b>Event Booking System</b>!
                    </p>
                    <p style="color: #888; font-size: 12px;">
                        Please arrive 30 minutes before the event.
                    </p>
                </div>

            </div>
        </body>
        </html>
        """,
        subtype = MessageType.html
    )
    fm = FastMail(conf)
    await fm.send_message(message)