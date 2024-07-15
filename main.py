from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend

from routers import live

app = FastAPI(docs_url=None, redoc_url=None)
FastAPICache.init(InMemoryBackend())

app.include_router(live.router)
