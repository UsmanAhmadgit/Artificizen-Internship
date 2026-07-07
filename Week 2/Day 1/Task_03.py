#3.	Add a GET /items route with optional query parameters skip (default 0) and limit (default 10) that return a fake paginated list.

from fastapi import FastAPI

app = FastAPI()

@app.get("/items")
def get_items(skip: int = 0, limit: int = 10):
    fake_database = [f"Item {i}" for i in range(1, 51)]
    paginated_items = fake_database[skip : skip + limit]
    
    return {
        "skip": skip,
        "limit": limit,
        "total_in_database": len(fake_database),
        "data": paginated_items
    }