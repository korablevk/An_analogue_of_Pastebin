import uvicorn
from contextlib import asynccontextmanager
import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_versioning import VersionedFastAPI
from redis import asyncio as aioredis

from app.config import settings
from app.database import engine
from app.logger import logger
from app.users.routher import router_users, router_auth
from app.pages.routher import router as router_pages


app = FastAPI(
    title="Pastebin",
    version="0.1.0",
    root_path="/api",
)

app.include_router(router_auth)
app.include_router(router_users)

origins = [
    # 3000 - порт, на котором работает фронтенд на React.js
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers",
                   "Access-Control-Allow-Origin", "Authorization"],
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # при запуске
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield
    # при выключении

app.include_router(router_pages)
app.mount("/static", StaticFiles(directory="app/static"), "static")


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info("Request handling time", extra={
        "process_time": round(process_time, 4)
    })
    return response


if __name__ == '__main__':
    uvicorn.run('app.main:app', host='127.0.0.1', port=8000, reload=True)