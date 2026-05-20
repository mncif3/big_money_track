from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import date, timedelta
from app.api.deps import get_db
from app.models.margin import MarginDaily

router = APIRouter(prefix="/api/margin", tags=["margin"])

@router.get("/summary")
async def margin_summary(period: str = Query("1m"), db: AsyncSession = Depends(get_db)):
    days = {"1w": 5, "1m": 20, "3m": 60}.get(period, 20)
    start = date.today() - timedelta(days=days * 2)
    stmt = select(MarginDaily).where(MarginDaily.trade_date >= start).order_by(MarginDaily.trade_date.asc())
    rows = (await db.execute(stmt)).scalars().all()
    return {"trend": [
        {"date": str(r.trade_date), "margin_balance": float(r.margin_balance or 0),
         "short_balance": float(r.short_balance or 0), "margin_net_buy": float(r.margin_net_buy or 0),
         "margin_ratio": float(r.margin_ratio or 0)}
        for r in rows
    ]}
