from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from fastapi import FastAPI

from config import settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, Any]:
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/", name="Get some", description="Get some info")
async def get_some() -> dict:
    db_url = settings.db.url
    return {"DB_URL": db_url}
