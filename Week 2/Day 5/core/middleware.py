from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware

# TASK 2: Request Logging Middleware
async def log_requests(request: Request, call_next):
    response = await call_next(request)
    print(f"API LOG: {request.method} {request.url.path} -> Status: {response.status_code}")
    return response

# TASK 3: CORS Configuration
def add_cors(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )