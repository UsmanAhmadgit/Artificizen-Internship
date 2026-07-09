from fastapi import FastAPI
from database import engine
import models

import Task_02
import Task_03
import Task_04
import Task_05
import Task_06

app = FastAPI(title="Artificizen Internship - Day 3")

# Task 1: Run Base.metadata.create_all() to create the tables in Postgres
models.Base.metadata.create_all(bind=engine)

app.include_router(Task_02.router)
app.include_router(Task_03.router)
app.include_router(Task_04.router)
app.include_router(Task_05.router)
app.include_router(Task_06.router)

@app.get("/", tags=["Root"])
def root():
    return {"message": "Master API is running. Go to /docs to test all tasks!"}