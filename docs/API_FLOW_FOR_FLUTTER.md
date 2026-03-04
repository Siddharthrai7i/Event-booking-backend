# Event Booking Backend – API Flow for Flutter

Single reference for the Flutter developer: app flow, all APIs, request/response shapes, and error handling.

---

## Base URL & Auth

| Item | Value |
|------|--------|
| **Base URL** | `http://<host>:8000` (e.g. `http://127.0.0.1:8000` or your deployed URL) |
| **API prefix** | All app APIs are under `/api/v1` |
| **Auth** | JWT Bearer token in header for protected routes |

**Protected routes** require:

```http
Authorization: Bearer <access_token>
```

**Important:** User must be **email-verified** before using booking/payment or `/auth/me`. Unverified users get `403` with detail *"Please verify your email first. Check your inbox for OTP."*

---

## App Flow (User Journey)

```
1. Sign up          → POST /api/v1/auth/signup
2. (Optional) Login → POST /api/v1/auth/login  (or use tokens from signup)
3. Verify email     → POST /api/v1/auth/send-otp  →  POST /api/v1/auth/verify-otp
4. Browse events    → GET /api/v1/events  →  GET /api/v1/events/{event_id}
5. Reserve seat     → POST /api/v1/booking/reserve  (body: seat_id)
6. Pay (Razorpay)   → POST /api/v1/payment/create-order  →  [Razorpay Checkout in app]  →  POST /api/v1/payment/verify
7. View bookings    → GET /api/v1/booking/my-bookings
```

Optional: cancel a **PENDING** reservation → `POST /api/v1/booking/cancel`.

---

## 1. Health (no auth)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Server health check |

**Response:** `200`  
```json
{ "status": "ok" }
```

---

## 2. Auth APIs

Base path: **`/api/v1/auth`**

### 2.1 Sign up (public)

**POST** `/api/v1/auth/signup`

**Request body:**
```json
{
  "email": "user@example.com",
  "password": "your_password"
}
```

**Success:** `201`  
```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer"
}
```

**Errors:**  
- `409` – Email already exists (`detail`: "An account with this email already exists")

---

### 2.2 Login (public)

**POST** `/api/v1/auth/login`

**Request body:**
```json
{
  "email": "user@example.com",
  "password": "your_password"
}
```

**Success:** `200`  
```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer"
}
```

**Errors:**  
- `401` – Invalid email or password

---

### 2.3 Refresh access token (public)

**POST** `/api/v1/auth/refresh`

**Request body:**
```json
{
  "refresh_token": "eyJ..."
}
```

**Success:** `200`  
```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer"
}
```

**Errors:**  
- `401` – Invalid or expired token

**Usage:** When `access_token` expires, call this with `refresh_token` and store the new tokens.

---

### 2.4 Send OTP (public)

**POST** `/api/v1/auth/send-otp`

**Request body:**
```json
{
  "email": "user@example.com"
}
```

**Success:** `200` – OTP sent to email (response body may be a simple message).

**Errors:**  
- `404` – No account with this email  
- `400` – Email already verified  

Use before **verify-otp** to complete email verification.

---

### 2.5 Verify OTP (public)

**POST** `/api/v1/auth/verify-otp`

**Request body:**
```json
{
  "email": "user@example.com",
  "otp": "123456"
}
```

**Success:** `200` – Email marked verified. User can now use protected booking/payment APIs.

**Errors:**  
- `400` – Invalid or expired OTP  
- `404` – No account with this email  

---

### 2.6 Get current user (protected)

**GET** `/api/v1/auth/me`  
**Header:** `Authorization: Bearer <access_token>`

**Success:** `200`  
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "role": "user",
  "is_verified": true
}
```

**Errors:**  
- `401` – Invalid or expired token  
- `403` – Email not verified  

---

## 3. Events APIs (public, no auth)

Base path: **`/api/v1/events`**

### 3.1 List events (paginated)

**GET** `/api/v1/events?page=1&limit=10`

| Query | Type | Default | Description |
|-------|------|---------|-------------|
| page  | int | 1  | Page number (≥ 1) |
| limit | int | 10 | Page size (1–100) |

**Success:** `200`  
```json
{
  "events": [
    {
      "id": "uuid",
      "name": "Concert Name",
      "city": "Mumbai",
      "venue": "Venue Name",
      "date": "2026-03-15T18:00:00"
    }
  ],
  "total": 25,
  "page": 1,
  "limit": 10
}
```

---

### 3.2 Get event details with seats

**GET** `/api/v1/events/{event_id}`

**Success:** `200`  
```json
{
  "event": {
    "id": "uuid",
    "name": "Concert Name",
    "city": "Mumbai",
    "venue": "Venue Name",
    "date": "2026-03-15T18:00:00"
  },
  "seats": {
    "VIP": {
      "price": 1500.0,
      "seats": [
        {
          "id": "seat-uuid",
          "seat_number": "A1",
          "status": "AVAILABLE",
          "price": 1500.0,
          "category": "VIP"
        }
      ]
    },
    "Standard": {
      "price": 500.0,
      "seats": [ ... ]
    }
  }
}
```

**Seat statuses:** `AVAILABLE` | `RESERVED` | `BOOKED`

**Errors:**  
- `404` – Event not found  

Use this to show event info and seat map; only **AVAILABLE** seats can be reserved.

---

## 4. Booking APIs (protected)

Base path: **`/api/v1/booking`**  
All require: **`Authorization: Bearer <access_token>`** and **verified email**.

### 4.1 Reserve a seat

**POST** `/api/v1/booking/reserve`

**Request body:**
```json
{
  "seat_id": "seat-uuid"
}
```

**Success:** `201`  
```json
{
  "id": "booking-uuid",
  "seat_id": "seat-uuid",
  "amount": 500.00,
  "status": "PENDING",
  "expires_at": "2026-03-04T12:20:00.000Z",
  "created_at": "2026-03-04T12:10:00.000Z"
}
```

**Booking status:** `PENDING` until payment succeeds; then `CONFIRMED`. If not paid before `expires_at`, backend may cancel it (typically ~10 minutes).

**Errors:**  
- `404` – Seat not found  
- `409` – Seat not available  
- `403` – Email not verified  

**Next step:** Use returned `id` (booking_id) for payment (create order → Razorpay → verify).

---

### 4.2 My bookings

**GET** `/api/v1/booking/my-bookings`

**Success:** `200`  
Array of booking objects (same shape as 4.1), newest first:
```json
[
  {
    "id": "booking-uuid",
    "seat_id": "seat-uuid",
    "amount": 500.00,
    "status": "CONFIRMED",
    "expires_at": "...",
    "created_at": "..."
  }
]
```

---

### 4.3 Get single booking

**GET** `/api/v1/booking/{booking_id}`

**Success:** `200` – Single booking object (same as 4.1).

**Errors:**  
- `404` – Booking not found  
- `403` – Booking does not belong to current user  

---

### 4.4 Cancel booking

**POST** `/api/v1/booking/cancel`

**Request body:**
```json
{
  "booking_id": "booking-uuid"
}
```

**Success:** `200`  
```json
{
  "message": "Booking cancelled successfully ✅"
}
```

**Errors:**  
- `404` – Booking not found  
- `403` – Booking not yours  
- `400` – Only PENDING bookings can be cancelled  

---

## 5. Payment APIs (protected, Razorpay)

Base path: **`/api/v1/payment`**  
All require: **`Authorization: Bearer <access_token>`** and **verified email**.

Recommended flow: **create-order** → open Razorpay Checkout in app → on success call **verify**.

### 5.1 Create Razorpay order

**POST** `/api/v1/payment/create-order`

**Request body:**
```json
{
  "booking_id": "booking-uuid"
}
```

**Success:** `200`  
```json
{
  "order_id": "order_xxxx",
  "key_id": "rzp_test_xxxx",
  "amount": 500.0,
  "amount_paise": 50000,
  "currency": "INR",
  "booking_id": "booking-uuid"
}
```

Use `order_id`, `key_id`, and `amount_paise` (or `amount`) in the Razorpay SDK (e.g. Flutter) to open checkout.

**Errors:**  
- `404` – Booking not found  
- `403` – Not your booking / email not verified  
- `400` – Booking already paid  
- `400` – Booking expired  
- `503` – Razorpay not configured (missing keys in backend)  

---

### 5.2 Verify payment (after Razorpay success)

**POST** `/api/v1/payment/verify`

Call this **after** Razorpay checkout succeeds. Pass the same `booking_id` and the values Razorpay returns in the success callback.

**Request body:**
```json
{
  "booking_id": "booking-uuid",
  "razorpay_payment_id": "pay_xxxx",
  "razorpay_order_id": "order_xxxx",
  "razorpay_signature": "signature_from_razorpay"
}
```

**Success:** `200`  
```json
{
  "status": "SUCCESS ✅",
  "message": "Payment successful! Booking confirmed. Check your email.",
  "booking_id": "booking-uuid",
  "payment_id": "payment-uuid",
  "amount_paid": 500.0,
  "booking_status": "CONFIRMED",
  "seat_status": "BOOKED"
}
```

**Errors:**  
- `400` – Invalid payment signature  
- `404` – Booking not found  
- `403` – Not your booking  
- `409` – Payment already processed (idempotent; safe to show success if you already verified)  

Verification is idempotent: calling verify again with the same `razorpay_payment_id` returns success and same data.

---

### 5.3 Get payment details

**GET** `/api/v1/payment/{booking_id}`

**Success:** `200`  
```json
{
  "id": "payment-uuid",
  "booking_id": "booking-uuid",
  "amount": 500.00,
  "status": "SUCCESS",
  "idempotency_key": "pay_xxxx",
  "created_at": "2026-03-04T12:25:00.000Z"
}
```

**Errors:**  
- `404` – Booking or payment not found  
- `403` – Not your booking  

---

### 5.4 Legacy simulated payment (optional, not for production)

**POST** `/api/v1/payment/pay`

**Request body:**
```json
{
  "booking_id": "booking-uuid",
  "idempotency_key": "unique-string-per-attempt"
}
```

Backend simulates success/failure. Prefer **create-order** + **verify** with Razorpay for real payments.

---

## 6. Standard error response

All API errors use a common shape:

```json
{
  "detail": "Human-readable message"
}
```

Sometimes `detail` is an array of validation errors. Always check HTTP status code and `detail` for user-facing messages.

---

## 7. Flow summary for Flutter

| Step | Action | API |
|------|--------|-----|
| 1 | Sign up | POST `/api/v1/auth/signup` |
| 2 | (Optional) Login | POST `/api/v1/auth/login` |
| 3 | Verify email | POST `/api/v1/auth/send-otp` → POST `/api/v1/auth/verify-otp` |
| 4 | Get profile / check auth | GET `/api/v1/auth/me` |
| 5 | List events | GET `/api/v1/events?page=1&limit=10` |
| 6 | Event detail + seats | GET `/api/v1/events/{event_id}` |
| 7 | Reserve seat | POST `/api/v1/booking/reserve` with `seat_id` |
| 8 | Create payment order | POST `/api/v1/payment/create-order` with `booking_id` |
| 9 | Open Razorpay Checkout | Use Razorpay Flutter SDK with `order_id`, `key_id`, amount |
| 10 | On payment success | POST `/api/v1/payment/verify` with `booking_id`, `razorpay_payment_id`, `razorpay_order_id`, `razorpay_signature` |
| 11 | Show my bookings | GET `/api/v1/booking/my-bookings` |
| 12 | Cancel (optional) | POST `/api/v1/booking/cancel` with `booking_id` (only PENDING) |

**Token handling:** Store `access_token` and `refresh_token`. Send `access_token` in `Authorization: Bearer <access_token>` on every protected request. On `401`, call POST `/api/v1/auth/refresh` with `refresh_token`, then retry the request with the new `access_token`.

---

## 8. Quick reference – all endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/health` | No | Health check |
| POST | `/api/v1/auth/signup` | No | Register |
| POST | `/api/v1/auth/login` | No | Login |
| POST | `/api/v1/auth/refresh` | No | Refresh token |
| POST | `/api/v1/auth/send-otp` | No | Send verification OTP |
| POST | `/api/v1/auth/verify-otp` | No | Verify OTP |
| GET | `/api/v1/auth/me` | Yes | Current user |
| GET | `/api/v1/events` | No | List events (paginated) |
| GET | `/api/v1/events/{event_id}` | No | Event + seats by category |
| POST | `/api/v1/booking/reserve` | Yes | Reserve seat |
| GET | `/api/v1/booking/my-bookings` | Yes | My bookings |
| GET | `/api/v1/booking/{booking_id}` | Yes | Booking details |
| POST | `/api/v1/booking/cancel` | Yes | Cancel PENDING booking |
| POST | `/api/v1/payment/create-order` | Yes | Create Razorpay order |
| POST | `/api/v1/payment/verify` | Yes | Verify Razorpay payment |
| GET | `/api/v1/payment/{booking_id}` | Yes | Payment details |
| POST | `/api/v1/payment/pay` | Yes | Legacy simulated pay |

**Auth = Yes** means: send `Authorization: Bearer <access_token>` and user must be email-verified.

---

*Document generated for Event Booking Backend. Use with Flutter (or any client) for full booking and Razorpay payment flow.*
