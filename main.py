import logging
import sys
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from config import settings
from database import sessionmanager

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG if settings.LOG_LEVEL == "DEBUG" else logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    if sessionmanager._engine is not None:
        # Close the DB connection
        await sessionmanager.close()


app = FastAPI(lifespan=lifespan, title='BZI', docs_url="/docs")


@app.get("/")
async def root():
    return {"message": "Hueta"}


# Routers


if __name__ == "__main__":
    uvicorn.run("main:app", host="172.30.56.144", reload=True, port=3019)
