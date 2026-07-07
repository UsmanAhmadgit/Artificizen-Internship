#2.	Add a GET /users/{user_id} route that returns the user ID as an integer. Test what happens when you pass a string.

from fastapi import FastAPI

app = FastAPI()

@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}