#1.	Create a FastAPI app with a GET / route that returns {"message": "Hello, Artificizen"}.

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello, Artificizen"}