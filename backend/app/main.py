from fastapi import FastAPI
from sqlalchemy import text

from app.database import engine

app = FastAPI(title="Simple Todo API", version="0.1.0")


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/health/db")
async def health_check_db():
    async with engine.connect() as conn:
        await conn.execute(text("SELECT 1"))
    return {"status": "healthy", "database": "connected"}
