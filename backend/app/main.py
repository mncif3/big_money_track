"""FastAPI 应用入口"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.db import engine
from app.scheduler import setup_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = setup_scheduler()
    scheduler.start()
    yield
    scheduler.shutdown(wait=False)
    await engine.dispose()


app = FastAPI(title="CapFlow — 股市资金流向监控系统", version="0.1.0", lifespan=lifespan)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True,
                   allow_methods=["*"], allow_headers=["*"])

from app.api.sectors import router as sectors_router
from app.api.stocks import router as stocks_router
from app.api.north import router as north_router
from app.api.south import router as south_router
from app.api.margin import router as margin_router
from app.api.alerts import router as alerts_router
from app.api.system import router as system_router
from app.api.main_thread import router as main_thread_router
from app.ws import router as ws_router

app.include_router(sectors_router)
app.include_router(stocks_router)
app.include_router(north_router)
app.include_router(south_router)
app.include_router(margin_router)
app.include_router(alerts_router)
app.include_router(system_router)
app.include_router(main_thread_router)
app.include_router(ws_router)


@app.get("/api/health")
async def health():
    return {"status": "ok", "version": "0.1.0"}
