# Day 5: Routers, Middleware, Error Handling & Testing

This project implements a modular, production-ready API architecture. Below is a structural breakdown of the core features and where to find their implementations within the codebase:

**`Task 1` (APIRouter):** Modular route definitions are handled in `routers/users.py` and `routers/auth.py`, and are centrally registered in `main.py`.
**`Task 2` (Logging Middleware):** Request logging logic is implemented inside `core/middleware.py` and attached to the application in `main.py`.
**`Task 3` (CORS Middleware):** Cross-Origin Resource Sharing is configured specifically for `http://localhost:3000` inside `core/middleware.py`.
**`Task 4` (Global Exceptions):** The custom exception handler for formatting unified JSON error responses is located in `core/exceptions.py`.
**`Task 5` (Background Tasks):** Non-blocking operations, such as the welcome email logic, are located inside the `POST /users/` route in `routers/users.py`.
**`Task 6` (Pytest):** The automated testing suite, which includes three distinct API test cases, is located in `tests/test_api.py`.