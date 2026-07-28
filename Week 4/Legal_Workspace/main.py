from fastapi import FastAPI
from routers import auth, rooms

app = FastAPI(
    title="AI Legal Case Workspace API",
    description="Multimodal RAG System for Legal Document Analysis",
)

app.include_router(auth.router)
app.include_router(rooms.router)

@app.get("/")
def read_root():
    return {"message": "API is running successfully. Navigate to /docs for Swagger UI."}