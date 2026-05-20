from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from datetime import date, timedelta
from app.api.deps import get_db
from app.models.fund_flow import SectorFundFlowDaily
from app.models.sector import Sector

router = APIRouter(prefix="/api/sectors", tags=["sectors"])

@router.get("/ranking")
async def sector_ranking(
    period: str = Query("1w", description="1d|1w|1m|3m|ytd"),
    limit: int = Query(10),
    direction: str = Query("in", description="in|out"),
    db: AsyncSession = Depends(get_db),
):
    days = {"1d": 1, "1w": 5, "1m": 20, "3m": 60, "ytd": 250}.get(period, 5)
    start = date.today() - timedelta(days=days * 2)

    subq = (
        select(
            SectorFundFlowDaily.sector_code,
            func.sum(SectorFundFlowDaily.main_net_inflow).label("total_inflow"),
            func.avg(SectorFundFlowDaily.main_net_ratio).label("avg_ratio"),
        )
        .where(SectorFundFlowDaily.trade_date >= start)
        .group_by(SectorFundFlowDaily.sector_code)
        .subquery()
    )
    order_col = subq.c.total_inflow.desc() if direction == "in" else subq.c.total_inflow.asc()
    stmt = (
        select(Sector.sector_name, subq.c.sector_code, subq.c.total_inflow, subq.c.avg_ratio)
        .join(subq, Sector.sector_code == subq.c.sector_code, isouter=True)
        .order_by(order_col)
        .limit(limit)
    )
    result = await db.execute(stmt)
    rows = result.all()
    return {"period": period, "ranking": [
        {"sector_code": r.sector_code, "sector_name": r.sector_name or r.sector_code,
         "total_inflow": float(r.total_inflow or 0), "avg_ratio": float(r.avg_ratio or 0)}
        for r in rows
    ]}

@router.get("/{code}/trend")
async def sector_trend(
    code: str,
    period: str = Query("1m"),
    db: AsyncSession = Depends(get_db),
):
    days = {"1w": 5, "1m": 20, "3m": 60}.get(period, 20)
    start = date.today() - timedelta(days=days * 2)
    stmt = (
        select(SectorFundFlowDaily)
        .where(SectorFundFlowDaily.sector_code == code, SectorFundFlowDaily.trade_date >= start)
        .order_by(SectorFundFlowDaily.trade_date.asc())
    )
    result = await db.execute(stmt)
    rows = result.scalars().all()
    return {"sector_code": code, "trend": [
        {"date": str(r.trade_date), "main_net_inflow": float(r.main_net_inflow or 0),
         "main_net_ratio": float(r.main_net_ratio or 0), "close_pct": float(r.close_pct or 0)}
        for r in rows
    ]}
