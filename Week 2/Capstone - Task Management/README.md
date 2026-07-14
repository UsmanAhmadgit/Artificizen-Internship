# Task Management REST API

A production-ready, modular REST API built with FastAPI and PostgreSQL. This project serves as an end-of-week capstone, demonstrating a secure, scalable backend architecture with strict user-data isolation and automated testing.

## Core Features

**Authentication & Security:** Secure user registration and login using bcrypt password hashing and JWT (JSON Web Token) authentication.

**Task Management (CRUD):** Complete Create, Read, Update, and Delete operations for tasks, strictly enforcing that users can only view and modify their own tasks.

**Domain-Driven Architecture:** Codebase organized by domains (security, database, routers) for maximum scalability and maintainability.

**Global Error Handling:** Custom exception handlers that standardize all HTTP errors into a predictable JSON format.

**Automated Testing:** Comprehensive test suite utilizing `pytest` and FastAPI's `TestClient` to verify core flows and unauthorized access barriers.

## Tech Stack

**Framework:** FastAPI
**Database:** PostgreSQL & SQLAlchemy (ORM)
**Authentication:** Passlib (Bcrypt) & Python-JOSE (JWT)
**Validation:** Pydantic
**Testing:** Pytest & HTTPX

## Project Structure

Capstone - Task Management/
├── core/
│   ├── security.py       # JWT logic, password hashing, and auth dependencies
│   └── exceptions.py     # Global JSON exception handler
├── db/
│   ├── database.py       # PostgreSQL connection and session management
│   ├── models.py         # SQLAlchemy ORM models (User, Task)
│   └── schemas.py        # Pydantic schemas for request/response validation
├── routers/
│   ├── auth.py           # Registration and login endpoints
│   └── tasks.py          # Task CRUD endpoints
├── tests/
│   └── test_api.py       # Automated integration tests
├── .env                  # Environment variables (Database URL, Secret Key)
└── main.py               # Application factory and router registration