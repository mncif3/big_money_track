"""主线判断 API"""
from fastapi import APIRouter, Query
from app.services.main_thread import get_top_sectors

router = APIRouter(prefix="/api/main-thread", tags=["main-thread"])


@router.get("")
async def main_thread(window: int = Query(20, description="时间窗口(交易日)")):
    return await get_top_sectors(top_n=3, window_days=window)
