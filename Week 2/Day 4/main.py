from fastapi import FastAPI

import Task_02
import Task_03
import Task_05
import Task_06

app = FastAPI(title="Artificizen Internship - Day 4 (Security)")

app.include_router(Task_02.router)
app.include_router(Task_03.router)
app.include_router(Task_05.router)
app.include_router(Task_06.router)

@app.get("/", tags=["Root"])
def root():
    return {"message": "Day 4 Security API is running."}