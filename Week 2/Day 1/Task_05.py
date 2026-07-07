#5.	Add a POST /ping route that returns status code 201 with {"status": "created"}.

from fastapi import FastAPI, status

app = FastAPI()

@app.post("/ping", status_code=status.HTTP_201_CREATED)
def ping():
    return {"status": "created"}