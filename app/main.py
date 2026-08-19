from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import db

from app.api import health, webhook

@asynccontextmanager
async def lifespan (app: FastAPI):
    db.init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(health.router)
app.include_router(webhook.router)
