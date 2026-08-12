from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.api import health
@asynccontextmanager
async def lifespan ():
    yield

app = FastAPI(lifespan)

app.include_router(health)



