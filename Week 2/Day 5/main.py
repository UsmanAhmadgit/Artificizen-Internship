from fastapi import FastAPI, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from routers import users, auth
from core.middleware import log_requests, add_cors
from core.exceptions import custom_http_exception_handler

app = FastAPI(title="Artificizen Internship - Day 5")

add_cors(app)

app.add_middleware(BaseHTTPMiddleware, dispatch=log_requests)

app.add_exception_handler(HTTPException, custom_http_exception_handler)

app.include_router(users.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Day 5 Modular Architecture Running"}
