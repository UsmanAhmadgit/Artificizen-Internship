from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

async def global_http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": True, "detail": exc.detail, "status": exc.status_code},
    )
