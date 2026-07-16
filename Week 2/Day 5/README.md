# Day 5 - FastAPI Modular Architecture

A focused FastAPI project demonstrating production-style API structure with routers, middleware, global error handling, background tasks, and basic test coverage.

## Table of Contents

- [Overview](#overview)
- [Implemented Tasks](#implemented-tasks)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [API Endpoints](#api-endpoints)
- [Run Tests](#run-tests)

## Overview

This day-5 exercise is designed to practice clean backend structure using FastAPI. The app is split into reusable modules and includes core patterns you would use in real projects.

## Implemented Tasks

| Task | Topic | Implementation |
| --- | --- | --- |
| 1 | APIRouter | `routers/users.py`, `routers/auth.py`, registered in `main.py` |
| 2 | Logging middleware | `core/middleware.py` via `BaseHTTPMiddleware` |
| 3 | CORS middleware | `core/middleware.py` configured for `http://localhost:3000` |
| 4 | Global exception handling | `core/exceptions.py` custom HTTP exception handler |
| 5 | Background tasks | Welcome email task in `POST /users/` |
| 6 | Pytest test suite | `tests/test_api.py` (3 API test cases) |

## Tech Stack

- FastAPI
- Starlette middleware
- Pytest
- Uvicorn

## Project Structure

```text
Day 5/
|-- core/
|   |-- exceptions.py
|   `-- middleware.py
|-- routers/
|   |-- auth.py
|   `-- users.py
|-- tests/
|   `-- test_api.py
|-- main.py
`-- README.md
```

## Getting Started

### 1) Create and activate virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 2) Install dependencies

```bash
pip install fastapi uvicorn pytest
```

### 3) Run the API

```bash
uvicorn main:app --reload
```

Open docs at:

- `http://127.0.0.1:8000/docs`
- `http://127.0.0.1:8000/redoc`

## API Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/` | Health/root message |
| POST | `/users/` | Create user and trigger background email task |
| GET | `/users/me` | Mock protected profile route (returns unauthorized in this exercise) |
| POST | `/auth/token` | Mock login route returning fake token |

## Run Tests

```bash
pytest -q
```

Expected coverage includes:

- successful user creation
- duplicate email conflict
- protected route access without token
