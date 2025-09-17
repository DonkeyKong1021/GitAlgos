from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.analytics.router import router as analytics_router
from app.auth.router import router as auth_router
from app.backtest.router import router as backtest_router
from app.data.router import router as data_router
from app.live.router import router as live_router
from app.sentiment.router import router as sentiment_router
from app.settings import settings
from app.strategies.router import router as strategies_router
from app.utils.logging import configure_logging, get_request_id

configure_logging()
app = FastAPI(title="AlgoForge Trading Engine")

origins = settings.cors_origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = get_request_id(request)
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


@app.get("/healthz")
async def healthz():
    return {"status": "ok", "time": datetime.utcnow().isoformat()}


app.include_router(auth_router)
app.include_router(strategies_router)
app.include_router(backtest_router)
app.include_router(live_router)
app.include_router(data_router)
app.include_router(sentiment_router)
app.include_router(analytics_router)
