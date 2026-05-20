import pandas as pd
import numpy as np
from datetime import date, timedelta
from sqlalchemy import select
from app.db import async_session
from app.models.fund_flow import SectorFundFlowDaily, StockFundFlowDaily

WEIGHTS = {"amount": 0.35, "persist": 0.25, "strength": 0.20, "accel": 0.10, "breadth": 0.10}

async def compute_sector_score(window_days: int = 20) -> pd.DataFrame:
    end = date.today()
    start = end - timedelta(days=window_days * 2)
    async with async_session() as sess:
        stmt = select(SectorFundFlowDaily).where(SectorFundFlowDaily.trade_date >= start)
        rows = (await sess.execute(stmt)).scalars().all()
    records = [{"sector_code": r.sector_code, "trade_date": r.trade_date,
                "main_net_inflow": float(r.main_net_inflow or 0),
                "main_net_ratio": float(r.main_net_ratio or 0)} for r in rows]
    df = pd.DataFrame(records)
    if df.empty:
        return pd.DataFrame()
    df = df.sort_values(["sector_code", "trade_date"])
    df = df.groupby("sector_code").tail(window_days)
    agg = df.groupby("sector_code").agg(
        amount_sum=("main_net_inflow", "sum"),
        persist_days=("main_net_inflow", lambda x: (x > 0).sum()),
        strength_mean=("main_net_ratio", "mean"),
        recent5=("main_net_inflow", lambda x: x.tail(5).mean() if len(x) >= 5 else x.mean()),
        window_mean=("main_net_inflow", "mean"),
    )
    agg["persist_score"] = agg["persist_days"] / window_days
    agg["accel"] = agg["recent5"] / agg["window_mean"].replace(0, 1e-9) - 1
    for col in ["amount_sum", "strength_mean", "accel"]:
        s = agg[col]
        agg[f"{col}_z"] = (s - s.mean()) / (s.std() + 1e-9)
    agg["score"] = (
        WEIGHTS["amount"] * agg["amount_sum_z"] +
        WEIGHTS["persist"] * agg["persist_score"] +
        WEIGHTS["strength"] * agg["strength_mean_z"] +
        WEIGHTS["accel"] * agg["accel_z"]
    )
    return agg.sort_values("score", ascending=False)

async def get_top_sectors(top_n: int = 3, window_days: int = 20):
    score_df = await compute_sector_score(window_days)
    if score_df.empty:
        return {"window_days": window_days, "top_sectors": [], "computed_at": str(date.today())}
    top = score_df.head(top_n)
    top_sectors = []
    for code, row in top.iterrows():
        top_sectors.append({
            "sector_code": code,
            "sector_name": code,
            "score": round(float(row["score"]), 2),
            "amount_sum": round(float(row["amount_sum"])),
            "persist_days": int(row["persist_days"]),
            "strength_mean": round(float(row["strength_mean"]), 4),
            "accel": round(float(row["accel"]), 4),
            "leaders": [],
        })
    return {"window_days": window_days, "top_sectors": top_sectors, "computed_at": str(date.today())}
