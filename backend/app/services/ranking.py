import pandas as pd
from datetime import date, timedelta
from sqlalchemy import select, func
from app.db import async_session
from app.models.fund_flow import SectorFundFlowDaily

async def get_sector_ranking(window_days: int = 20, top_n: int = 10) -> pd.DataFrame:
    end = date.today()
    start = end - timedelta(days=window_days * 2)
    async with async_session() as sess:
        stmt = select(SectorFundFlowDaily).where(SectorFundFlowDaily.trade_date >= start)
        rows = (await sess.execute(stmt)).scalars().all()
    df = pd.DataFrame([{
        "sector_code": r.sector_code, "trade_date": r.trade_date,
        "main_net_inflow": float(r.main_net_inflow or 0),
        "main_net_ratio": float(r.main_net_ratio or 0),
    } for r in rows])
    if df.empty:
        return pd.DataFrame()
    df = df.sort_values(["sector_code", "trade_date"])
    df = df.groupby("sector_code").tail(window_days)
    agg = df.groupby("sector_code").agg(
        total_inflow=("main_net_inflow", "sum"),
        avg_ratio=("main_net_ratio", "mean"),
        inflow_days=("main_net_inflow", lambda x: (x > 0).sum()),
    ).reset_index()
    agg["score"] = agg["total_inflow"].rank(ascending=False)
    return agg.sort_values("total_inflow", ascending=False).head(top_n)
