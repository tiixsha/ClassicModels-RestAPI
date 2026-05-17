# ClassicModels REST API

A fully-featured RESTful API built with **FastAPI** and **PostgreSQL** for managing the ClassicModels database. This project was developed across four progressive tasks covering database setup, CRUD operations, concurrency, and full API coverage.

## Table of Contents

- [Project Overview](#project-overview)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Task Breakdown](#task-breakdown)
- [API Endpoints](#api-endpoints)
- [Design Decisions](#design-decisions)

## Tech Stack

- **FastAPI** — Web framework and API routing
- **PostgreSQL** — Relational database
- **SQLAlchemy** — ORM for database interaction
- **Pydantic** — Request/response validation and serialization
- **Docker / Docker Compose** — Containerized database setup
- **Python-dotenv** — Secure environment variable management
- **Uvicorn** — ASGI server

## Project Structure

ClassicModels-RestAPI/
│
├── database.py           # DB engine, session management, get_db()
├── models.py             # SQLAlchemy ORM models for all tables
├── main.py               # FastAPI app entry point, router registration
├── seed.sql              # Database seed file
├── docker-compose.yml    # PostgreSQL container configuration
├── .env                  # Environment variables (not committed)
├── requirements.txt      # Python dependencies
│
├── routers/
│   ├── customer_router.py
│   ├── product_router.py
│   ├── productline_router.py
│   ├── office_router.py
│   ├── employee_router.py
│   ├── order_router.py
│   ├── orderdetail_router.py
│   ├── payment_router.py
│   └── dashboard_router.py
│
├── crud/
│   ├── customer_crud.py
│   ├── product_crud.py
│   ├── productline_crud.py
│   ├── office_crud.py
│   ├── employee_crud.py
│   ├── order_crud.py
│   ├── orderdetail_crud.py
│   └── payment_crud.py
│
└── schemas/
    ├── customer_schemas.py
    ├── product_schemas.py
    ├── productline_schemas.py
    ├── office_schemas.py
    ├── employee_schemas.py
    ├── order_schemas.py
    ├── orderdetail_schemas.py
    └── payment_schemas.py

## Getting Started

### Prerequisites

- Docker and Docker Compose installed
- Python 3.10+

### 1. Clone the repository

```bash
git clone https://github.com/tiixsha/ClassicModels-RestAPI.git
cd ClassicModels-RestAPI
```

### 2. Set up environment variables

Create a `.env` file in the root directory:

```
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password
POSTGRES_DB=mydb
POSTGRES_PORT=5432
DATABASE_URL=postgresql://your_username:your_password@localhost:5432/mydb
```

### 3. Start the database

```bash
docker-compose up -d
```

This spins up a PostgreSQL container, runs the `seed.sql` file automatically, and persists data using a named Docker volume.

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the API

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
### 6. API Layers

The API is organized into four layers:

| Layer | File | Responsibility |
|---|---|---|
| Connection | `database.py` | Engine, sessions, `get_db()` |
| Models | `models.py` | SQLAlchemy ORM table definitions |
| Schemas | `schemas.py` | Pydantic validation and serialization |
| CRUD | `crud.py` | Database operations |
| Routes | `router.py` | HTTP endpoints |

## API Endpoints

| Resource | Base Path |
|---|---|
| Customers | `/customers` |
| Products | `/products` |
| Product Lines | `/productlines` |
| Offices | `/offices` |
| Employees | `/employees` |
| Orders | `/orders` |
| Order Details | `/orderdetails` |
| Payments | `/payments` |
| Dashboard | `/overall_counts` |
