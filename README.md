# 🎫 Event Booking System

A production-ready backend API built with **FastAPI**, inspired by BookMyShow.
Handles user auth, event browsing, seat reservation, payments, and email notifications.

---

## 🏗️ Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Migrations | Alembic |
| Cache / OTP Store | Redis |
| Auth | JWT (access + refresh tokens) |
| Password Hashing | bcrypt (passlib) |
| Email | fastapi-mail (Gmail SMTP) |
| OTP | pyotp |
| Task Queue | Celery |
| Dependency Manager | Poetry |
| Server | Uvicorn |

---

## 📁 Folder Structure

```
event-booking-system/
│
├── app/
│   ├── main.py                        # FastAPI app entry point
│   │
│   ├── core/
│   │   ├── config.py                  # Settings via pydantic BaseSettings
│   │   ├── security.py                # JWT creation, bcrypt hashing
│   │   └── dependencies.py            # get_current_user, get_db
│   │
│   ├── db/
│   │   ├── base.py                    # SQLAlchemy Base, engine, SessionLocal
│   │   ├── session.py                 # get_db() dependency
│   │   └── redis.py                   # Redis async client
│   │
│   ├── models/
│   │   ├── user.py                    # User model
│   │   ├── event.py                   # Event model
│   │   ├── seat.py                    # Seat model + SeatStatus enum
│   │   ├── booking.py                 # Booking model + BookingStatus enum
│   │   └── payment.py                 # Payment model + PaymentStatus enum
│   │
│   ├── schemas/
│   │   ├── auth.py                    # LoginRequest, SignupRequest, TokenResponse
│   │   ├── event.py                   # EventOut, EventListResponse
│   │   ├── booking.py                 # ReserveRequest, BookingOut
│   │   └── payment.py                 # PayRequest, PaymentOut
│   │
│   ├── api/
│   │   └── v1/
│   │       ├── router.py              # Aggregates all v1 routers
│   │       ├── auth.py                # Auth routes
│   │       ├── events.py              # Event routes
│   │       ├── booking.py             # Booking routes
│   │       └── payment.py             # Payment routes
│   │
│   ├── services/
│   │   ├── auth_service.py            # Login, signup, OTP logic
│   │   ├── event_service.py           # Fetch events, Redis cache
│   │   ├── booking_service.py         # Reserve seat, row lock
│   │   └── payment_service.py         # Process payment, idempotency
│   │
│   ├── repositories/
│   │   ├── user_repo.py               # User DB queries
│   │   ├── event_repo.py              # Event DB queries
│   │   ├── seat_repo.py               # Seat DB queries
│   │   ├── booking_repo.py            # Booking DB queries
│   │   └── payment_repo.py            # Payment DB queries
│   │
│   ├── workers/
│   │   ├── celery_app.py              # Celery setup
│   │   ├── tasks.py                   # send_confirmation_email task
│   │   └── email_utils.py             # Email templates
│   │
│   └── utils/
│       ├── otp.py                     # OTP generate + verify
│       ├── email.py                   # Send OTP email
│       ├── idempotency.py             # Idempotency key logic
│       ├── exceptions.py              # Custom HTTP exceptions
│       └── logger.py                  # Logging setup
│
├── migrations/
│   ├── env.py                         # Alembic environment config
│   ├── script.py.mako                 # Migration file template
│   └── versions/
│       ├── 0001_create_users_table.py
│       ├── 0002_add_is_verified_to_users.py
│       └── ...
│
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_events.py
│   ├── test_booking.py
│   └── test_payment.py
│
├── .env                               # Environment variables (never commit)
├── .env.example                       # Template for .env
├── alembic.ini                        # Alembic config
├── pyproject.toml                     # Poetry dependencies
├── poetry.lock                        # Locked dependency versions
├── docker-compose.yml                 # PostgreSQL + Redis + App
├── Dockerfile                         # App container
└── README.md
```

---

## ⚙️ Environment Variables

Create a `.env` file in the root folder:

```env
# Database
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/eventdb

# Redis
REDIS_URL=redis://localhost:6379

# JWT
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# Email (Gmail)
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_gmail_app_password
MAIL_FROM=your_email@gmail.com
MAIL_PORT=587
MAIL_SERVER=smtp.gmail.com
```

> ⚠️ Never commit `.env` to Git. It's already in `.gitignore`.

---

## 🚀 Getting Started

### Prerequisites

Make sure these are installed on your machine:

- Python 3.11+
- PostgreSQL
- Redis
- Poetry

---

### Step 1 — Clone the project

```cmd
git clone https://github.com/your-username/event-booking-system.git
cd event-booking-system
```

---

### Step 2 — Install dependencies

```cmd
poetry install
```

---

### Step 3 — Setup PostgreSQL

Open psql and create the database:

```cmd
psql -U postgres
```

```sql
CREATE DATABASE eventdb;
\q
```

---

### Step 4 — Setup Redis

Make sure Redis is running:

```cmd
redis-cli ping
```

Should return `PONG`. If not, start Redis:

```cmd
redis-server
```

---

### Step 5 — Configure environment

Copy the example env file:

```cmd
copy .env.example .env
```

Fill in your actual values in `.env`.

---

### Step 6 — Run database migrations

```cmd
poetry run alembic upgrade head
```

---

### Step 7 — Start the server

```cmd
poetry run uvicorn app.main:app --reload
```

Server runs at: **http://127.0.0.1:8000**

Swagger UI: **http://127.0.0.1:8000/docs**

---

## 📡 API Endpoints

### 🔐 Auth

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| POST | `/api/v1/auth/signup` | Register new user | ❌ |
| POST | `/api/v1/auth/login` | Login, get tokens | ❌ |
| POST | `/api/v1/auth/refresh` | Refresh access token | ❌ |
| GET | `/api/v1/auth/me` | Get current user info | ✅ |
| POST | `/api/v1/auth/send-otp` | Send OTP to email | ❌ |
| POST | `/api/v1/auth/verify-otp` | Verify OTP, activate account | ❌ |

### 🎫 Events

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| GET | `/api/v1/events` | List all events (paginated) | ❌ |
| GET | `/api/v1/events/{id}` | Get single event details | ❌ |

### 🎟️ Booking

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| POST | `/api/v1/booking/reserve` | Reserve a seat | ✅ |
| GET | `/api/v1/booking/{id}` | Get booking details | ✅ |

### 💳 Payment

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| POST | `/api/v1/payment/pay` | Pay for booking | ✅ |

---

## 🔄 Complete User Flow

```
1. POST /auth/signup          → Register with email + password
         ↓
2. POST /auth/send-otp        → OTP sent to email (valid 5 min)
         ↓
3. POST /auth/verify-otp      → Account verified ✅
         ↓
4. POST /auth/login           → Get access_token + refresh_token
         ↓
5. GET  /events               → Browse available events
         ↓
6. POST /booking/reserve      → Reserve a seat (status = PENDING)
         ↓
7. POST /payment/pay          → Pay for booking (status = CONFIRMED)
         ↓
8. Email sent async           → Confirmation email via queue
```

---

## 🗄️ Database Schema

### users
| Column | Type | Notes |
|---|---|---|
| id | UUID | Primary Key |
| email | VARCHAR(255) | UNIQUE, NOT NULL |
| password_hash | VARCHAR(255) | bcrypt hash |
| role | ENUM | user / admin |
| is_verified | BOOLEAN | default false |
| created_at | TIMESTAMP | default now() |

### events
| Column | Type | Notes |
|---|---|---|
| id | UUID | Primary Key |
| name | VARCHAR(255) | NOT NULL |
| city | VARCHAR(100) | |
| date | TIMESTAMP | Event datetime |
| venue | VARCHAR(255) | |

### seats
| Column | Type | Notes |
|---|---|---|
| id | UUID | Primary Key |
| event_id | UUID | FK → events.id |
| seat_number | VARCHAR(20) | e.g. A12 |
| status | ENUM | AVAILABLE / RESERVED / BOOKED |

### bookings
| Column | Type | Notes |
|---|---|---|
| id | UUID | Primary Key |
| user_id | UUID | FK → users.id |
| seat_id | UUID | FK → seats.id |
| status | ENUM | PENDING / CONFIRMED / CANCELLED |
| payment_id | UUID | FK → payments.id |
| created_at | TIMESTAMP | |

### payments
| Column | Type | Notes |
|---|---|---|
| id | UUID | Primary Key |
| booking_id | UUID | FK → bookings.id |
| amount | DECIMAL(10,2) | |
| status | ENUM | SUCCESS / FAILED |
| idempotency_key | VARCHAR(255) | UNIQUE |
| created_at | TIMESTAMP | |

---

## 🔑 Authentication

The API uses **JWT Bearer tokens**.

### How to use in Swagger:

1. Call `POST /api/v1/auth/login`
2. Copy the `access_token` from the response
3. Click the 🔒 **Authorize** button at the top of `/docs`
4. Paste the token and click **Authorize**
5. All protected routes now work automatically

### Token expiry:

| Token | Expiry |
|---|---|
| access_token | 15 minutes |
| refresh_token | 7 days |

When access_token expires, call `POST /auth/refresh` with your refresh_token to get a new one.

---

## 📧 Gmail App Password Setup

Gmail blocks direct password login. You need an **App Password**:

```
1. Go to myaccount.google.com
2. Security → 2-Step Verification → Enable
3. Security → App Passwords
4. Select: Mail + Windows Computer
5. Copy the 16-character password
6. Add to .env as MAIL_PASSWORD
```

---

## 🗃️ Alembic Migration Commands

```cmd
# Apply all pending migrations
poetry run alembic upgrade head

# Create a new migration (auto-detect model changes)
poetry run alembic revision --autogenerate --rev-id 000X -m "description"

# Rollback one migration
poetry run alembic downgrade -1

# Rollback everything
poetry run alembic downgrade base

# Check current migration status
poetry run alembic current

# View migration history
poetry run alembic history --verbose
```

### Migration naming convention:
```
0001_create_users_table.py
0002_add_is_verified_to_users.py
0003_create_events_table.py
0004_create_seats_table.py
0005_create_bookings_table.py
0006_create_payments_table.py
```

> ⚠️ Every time you add a new model, import it in `migrations/env.py` before running autogenerate.

---

## 🧪 Running Tests

```cmd
poetry run pytest
```

Run specific test file:

```cmd
poetry run pytest tests/test_auth.py -v
```

Run with coverage:

```cmd
poetry run pytest --cov=app tests/
```

---

## 🐳 Docker Setup

Start PostgreSQL + Redis with Docker:

```cmd
docker-compose up -d
```

Or run just the database:

```cmd
docker run --name eventdb \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=root \
  -e POSTGRES_DB=eventdb \
  -p 5432:5432 -d postgres
```

Run just Redis:

```cmd
docker run --name redis -p 6379:6379 -d redis
```

---

## 🛠️ Daily Development Commands

```cmd
# Always run from root folder
cd C:\Users\Admin\Desktop\event-booking-system

# Activate poetry shell
poetry shell

# Start server with hot reload
poetry run uvicorn app.main:app --reload

# Check where you are (must be root folder)
cd

# Apply new migrations
poetry run alembic upgrade head

# Add new package
poetry add package-name

# View installed packages
poetry show
```

---

## ❗ Common Errors & Fixes

| Error | Cause | Fix |
|---|---|---|
| `ModuleNotFoundError: No module named 'app'` | Wrong folder | `cd C:\Users\Admin\Desktop\event-booking-system` |
| `password authentication failed` | Wrong DB credentials | Check `DATABASE_URL` in `.env` |
| `column does not exist` | Migration not applied | `poetry run alembic upgrade head` |
| `error reading bcrypt version` | bcrypt too new | `poetry add bcrypt==4.0.1` |
| `Connection refused` (Redis) | Redis not running | `redis-server` |
| `PONG` not returned | Redis not running | Start Redis first |

---

## 📌 Key Design Decisions

**Layered Architecture** — Routes never touch the DB directly. Flow is always `route → service → repository → model`.

**Row-level locking** — Seat reservation uses `SELECT FOR UPDATE` to prevent double booking under concurrent requests.

**Idempotency keys** — Payment endpoint checks idempotency key before processing to prevent duplicate charges.

**Redis for OTP** — OTP secrets stored in Redis with 5-minute TTL. Auto-deleted after expiry — no manual cleanup needed.

**Async email** — Confirmation emails sent via Celery worker after payment. User does not wait for email delivery.

---

## 🔮 Upcoming Features

- [ ] Events service with Redis caching
- [ ] Seat reservation with row locks
- [ ] Payment service with idempotency
- [ ] Celery async email worker
- [ ] Admin dashboard routes
- [ ] Rate limiting
- [ ] Docker Compose full setup

---

## 👨‍💻 Author

Built with FastAPI + PostgreSQL + Redis