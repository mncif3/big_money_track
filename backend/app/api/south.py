from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import date, timedelta
from app.api.deps import get_db
from app.models.south import SouthCapitalDaily, SouthTop10Daily

router = APIRouter(prefix="/api/south", tags=["south"])

@router.get("/summary")
async def south_summary(period: str = Query("1m"), db: AsyncSession = Depends(get_db)):
    days = {"1w": 5, "1m": 20, "3m": 60}.get(period, 20)
    start = date.today() - timedelta(days=days * 2)
    stmt = select(SouthCapitalDaily).where(SouthCapitalDaily.trade_date >= start).order_by(SouthCapitalDaily.trade_date.asc())
    rows = (await db.execute(stmt)).scalars().all()
    return {"trend": [
        {"date": str(r.trade_date), "sh_net": float(r.sh_net_inflow or 0),
         "sz_net": float(r.sz_net_inflow or 0), "total_net": float(r.total_net_inflow or 0),
         "ah_premium": float(r.ah_premium or 0)}
        for r in rows
    ]}

@router.get("/top10")
async def south_top10(date_param: str = Query(None, alias="date"), db: AsyncSession = Depends(get_db)):
    target = date.fromisoformat(date_param) if date_param else date.today()
    stmt = select(SouthTop10Daily).where(SouthTop10Daily.trade_date == target).order_by(SouthTop10Daily.channel, SouthTop10Daily.rank)
    rows = (await db.execute(stmt)).scalars().all()
    return [{"channel": r.channel, "rank": r.rank, "stock_code": r.stock_code,
             "net_amount": float(r.net_amount or 0)} for r in rows]
