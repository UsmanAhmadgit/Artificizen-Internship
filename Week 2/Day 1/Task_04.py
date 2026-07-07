#4.	Raise an HTTPException with status 404 and a custom message when a user ID greater than 100 is requested.

from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/users/{user_id}")
def get_user_with_error(user_id: int):
    if user_id > 100:
        raise HTTPException(status_code=404, detail="User ID cannot be greater than 100")
    return {"user_id": user_id}