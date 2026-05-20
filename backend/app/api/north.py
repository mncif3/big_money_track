from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from datetime import date, timedelta
from app.api.deps import get_db
from app.models.north import NorthCapitalDaily, NorthTop10Daily

router = APIRouter(prefix="/api/north", tags=["north"])

@router.get("/summary")
async def north_summary(period: str = Query("1m"), db: AsyncSession = Depends(get_db)):
    days = {"1w": 5, "1m": 20, "3m": 60}.get(period, 20)
    start = date.today() - timedelta(days=days * 2)
    stmt = select(NorthCapitalDaily).where(NorthCapitalDaily.trade_date >= start).order_by(NorthCapitalDaily.trade_date.asc())
    rows = (await db.execute(stmt)).scalars().all()
    return {"trend": [
        {"date": str(r.trade_date), "sh_net": float(r.sh_net_inflow or 0),
         "sz_net": float(r.sz_net_inflow or 0), "total_net": float(r.total_net_inflow or 0)}
        for r in rows
    ]}

@router.get("/top10")
async def north_top10(date_param: str = Query(None, alias="date"), db: AsyncSession = Depends(get_db)):
    target = date.fromisoformat(date_param) if date_param else date.today()
    stmt = select(NorthTop10Daily).where(NorthTop10Daily.trade_date == target).order_by(NorthTop10Daily.channel, NorthTop10Daily.rank)
    rows = (await db.execute(stmt)).scalars().all()
    return [{"channel": r.channel, "rank": r.rank, "stock_code": r.stock_code,
             "net_amount": float(r.net_amount or 0)} for r in rows]
