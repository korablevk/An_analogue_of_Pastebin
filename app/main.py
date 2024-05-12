import uvicorn
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_versioning import VersionedFastAPI
from redis import asyncio as aioredis
from starlette.middleware.sessions import SessionMiddleware

from app.config import settings
from app.database import engine
from app.logger import logger
from app.users.routher import router_users, router_auth
from app.pastes.routher import router_pastes
from app.pages.routher import router as router_pages

app = FastAPI(
    title="Pastebin",
    version="0.1.0",
    root_path="/api",
)

origins = [
    '*'
]

app.add_middleware(SessionMiddleware, secret_key=settings.JWT_SECRET_KEY)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router_auth)
app.include_router(router_users)
app.include_router(router_pastes)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # при запуске
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield
    # при выключении

app.include_router(router_pages)
app.mount("/static", StaticFiles(directory="app/static"), "static")


# @app.middleware("http")
# async def some_middleware(request: Request, call_next):
#     response = await call_next(request)
#     session = request.cookies.get(settings.JWT_SECRET_KEY)
#     if session:
#         response.set_cookie(key=settings.JWT_SECRET_KEY, value=request.cookies.get(settings.JWT_SECRET_KEY), httponly=True)
#     return response


if __name__ == '__main__':
    uvicorn.run('app.main:app', host='127.0.0.1', port=8000, reload=True)