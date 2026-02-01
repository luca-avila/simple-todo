from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

from app.database import Base, engine
from app.models.user import User  # noqa: F401 - needed for metadata
from app.routers import auth


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="Simple Todo API", version="0.1.0", lifespan=lifespan)

app.include_router(auth.router)


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/health/db")
async def health_check_db():
    async with engine.connect() as conn:
        await conn.execute(text("SELECT 1"))
    return {"status": "healthy", "database": "connected"}
