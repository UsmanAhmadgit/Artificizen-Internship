# Task Management REST API

A modular FastAPI + PostgreSQL backend built as a capstone project. It includes secure authentication, task CRUD operations, per-user data isolation, global exception handling, and API tests.

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Environment Variables](#environment-variables)
- [Running the App](#running-the-app)
- [API Endpoints](#api-endpoints)
- [Run Tests](#run-tests)

## Features

- User registration and login
- JWT-based authentication
- Password hashing with bcrypt
- Full task CRUD (create, list, get, update, delete)
- Strict ownership checks so users only access their own tasks
- Optional task filtering by status
- Centralized JSON error responses
- Integration tests with FastAPI TestClient

## Tech Stack

- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- Passlib (bcrypt)
- Python-JOSE (JWT)
- Pytest

## Project Structure

```text
Capstone - Task Management/
|-- core/
|   |-- exceptions.py
|   `-- security.py
|-- db/
|   |-- database.py
|   |-- models.py
|   `-- schemas.py
|-- routers/
|   |-- auth.py
|   `-- tasks.py
|-- tests/
|   `-- test_api.py
|-- .env
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
pip install fastapi uvicorn sqlalchemy psycopg2-binary pydantic python-jose passlib[bcrypt] python-multipart pytest httpx
```

## Environment Variables

Create a `.env` file in the project root and define:

| Variable | Description | Example |
| --- | --- | --- |
| `DATABASE_URL` | PostgreSQL connection URL | `postgresql://postgres:password@localhost:5432/taskdb` |
| `SECRET_KEY` | JWT signing key | `super-secret-key` |


## Running the App

```bash
uvicorn main:app --reload
```

Open docs at:

- `http://127.0.0.1:8000/docs`
- `http://127.0.0.1:8000/redoc`

## API Endpoints

### Authentication

| Method | Endpoint | Description |
| --- | --- | --- |
| POST | `/auth/register` | Register a new user |
| POST | `/auth/token` | Login and get access token |

### Tasks (JWT required)

| Method | Endpoint | Description |
| --- | --- | --- |
| POST | `/tasks/` | Create task |
| GET | `/tasks/` | List current user's tasks |
| GET | `/tasks/{task_id}` | Get single task |
| PUT | `/tasks/{task_id}` | Update task |
| DELETE | `/tasks/{task_id}` | Delete task |

Filter support:

- `GET /tasks/?status=pending`
- `GET /tasks/?status=completed`

## Run Tests

```bash
pytest -q
```

Current tests verify:

- user registration
- login and token generation
- unauthorized access protection
- task creation
- task retrieval