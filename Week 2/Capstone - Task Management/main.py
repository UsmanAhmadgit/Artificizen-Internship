from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from db.database import engine, Base
from routers import auth, tasks
from core.exceptions import global_http_exception_handler

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Management API", description="End-of-Week Capstone")

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Exception Handler
app.add_exception_handler(HTTPException, global_http_exception_handler)

# Register Routers
app.include_router(auth.router)
app.include_router(tasks.router)
