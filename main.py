from fastapi import FastAPI
from routers import live

app = FastAPI(docs_url=None, redoc_url=None)

app.include_router(live.router)
