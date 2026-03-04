from sqlalchemy.orm import Session
from app.models.payment import Payment, PaymentStatus
import uuid

def get_payment_by_idempotency_key(db: Session, key: str) -> Payment | None:
    return db.query(Payment)\
             .filter(Payment.idempotency_key == key)\
             .first()

def get_payment_by_booking_id(db: Session, booking_id: str) -> Payment | None:
    return db.query(Payment)\
             .filter(Payment.booking_id == booking_id)\
             .first()

def get_payment_by_razorpay_payment_id(db: Session, razorpay_payment_id: str) -> Payment | None:
    return db.query(Payment)\
             .filter(Payment.razorpay_payment_id == razorpay_payment_id)\
             .first()

def create_payment(
    db                   : Session,
    booking_id           : str,
    amount               : float,
    status               : PaymentStatus,
    idempotency_key      : str,
    razorpay_order_id    : str | None = None,
    razorpay_payment_id  : str | None = None,
) -> Payment:
    payment = Payment(
        id                  = uuid.uuid4(),
        booking_id          = booking_id,
        amount              = amount,
        status              = status,
        idempotency_key     = idempotency_key,
        razorpay_order_id   = razorpay_order_id,
        razorpay_payment_id = razorpay_payment_id,
    )
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment