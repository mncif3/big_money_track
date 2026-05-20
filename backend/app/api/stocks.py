from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from datetime import date, timedelta
from app.api.deps import get_db
from app.models.fund_flow import StockFundFlowDaily
from app.models.stock import Stock

router = APIRouter(prefix="/api/stocks", tags=["stocks"])

@router.get("/{code}/flow")
async def stock_flow(code: str, period: str = Query("1m"), db: AsyncSession = Depends(get_db)):
    days = {"1w": 5, "1m": 20, "3m": 60}.get(period, 20)
    start = date.today() - timedelta(days=days * 2)
    stmt = (select(StockFundFlowDaily)
            .where(StockFundFlowDaily.stock_code == code, StockFundFlowDaily.trade_date >= start)
            .order_by(StockFundFlowDaily.trade_date.asc()))
    rows = (await db.execute(stmt)).scalars().all()
    return {"stock_code": code, "trend": [
        {"date": str(r.trade_date), "close_price": float(r.close_price or 0),
         "main_net_inflow": float(r.main_net_inflow or 0),
         "main_net_ratio": float(r.main_net_ratio or 0)}
        for r in rows
    ]}

@router.get("/{code}/profile")
async def stock_profile(code: str, db: AsyncSession = Depends(get_db)):
    stmt = select(Stock).where(Stock.stock_code == code)
    r = (await db.execute(stmt)).scalar_one_or_none()
    if not r:
        return {"error": "not found"}
    return {"stock_code": r.stock_code, "stock_name": r.stock_name,
            "market": r.market, "list_date": str(r.list_date) if r.list_date else None}
