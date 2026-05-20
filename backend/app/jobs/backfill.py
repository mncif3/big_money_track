"""历史数据回填脚本 — 动态获取板块代码并回填"""
import asyncio
import logging
import akshare as ak
import pandas as pd
from datetime import date, datetime
from sqlalchemy.dialects.postgresql import insert
from app.db import async_session
from app.models.fund_flow import SectorFundFlowDaily
from app.models.sector import Sector

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def fetch_sectors():
    """从 akshare 获取申万行业板块列表"""
    try:
        df = await asyncio.to_thread(ak.stock_board_industry_name_em)
        return [(row.get("板块代码", ""), row.get("板块名称", "")) for _, row in df.iterrows()]
    except Exception as e:
        logger.error(f"Failed to fetch sectors: {e}")
        return []


async def backfill_sector(symbol: str, name: str, start_date: str = "20250101"):
    try:
        # Save sector metadata
        async with async_session() as sess:
            stmt = insert(Sector).values(
                sector_code=symbol, sector_name=name, sector_type="industry", is_active=True
            ).on_conflict_do_update(
                index_elements=["sector_code"],
                set_={"sector_name": name, "updated_at": datetime.now()}
            )
            await sess.execute(stmt)
            await sess.commit()

        # Fetch historical fund flow
        df = await asyncio.to_thread(ak.stock_sector_fund_flow_hist, symbol=symbol)
        if df is None or df.empty:
            return 0

        col_map = {
            "日期": "trade_date", "主力净流入-净额": "main_net_inflow",
            "主力净流入-净占比": "main_net_ratio", "超大单净流入-净额": "super_large_net",
            "大单净流入-净额": "large_net", "中单净流入-净额": "medium_net",
            "小单净流入-净额": "small_net", "成交额": "turnover", "涨跌幅": "close_pct"
        }
        df = df.rename(columns={k: v for k, v in col_map.items() if k in df.columns})

        records = []
        for _, row in df.iterrows():
            td = row.get("trade_date", "")
            if isinstance(td, str):
                try:
                    td = datetime.strptime(td, "%Y-%m-%d").date()
                except ValueError:
                    continue
            elif hasattr(td, "date"):
                td = td.date()
            if not isinstance(td, date) or td < date(2025, 1, 1):
                continue

            rec = {"trade_date": td, "sector_code": symbol, "data_source": "akshare"}
            for col in ["main_net_inflow", "main_net_ratio", "super_large_net",
                        "large_net", "medium_net", "small_net", "turnover", "close_pct"]:
                if col in df.columns:
                    rec[col] = float(row[col]) if pd.notna(row[col]) else 0
            records.append(rec)

        if records:
            async with async_session() as sess:
                stmt = insert(SectorFundFlowDaily).values(records)
                stmt = stmt.on_conflict_do_update(
                    index_elements=["trade_date", "sector_code"],
                    set_={c.name: stmt.excluded[c.name] for c in SectorFundFlowDaily.__table__.columns
                          if c.name not in ("trade_date", "sector_code", "created_at")}
                )
                await sess.execute(stmt)
                await sess.commit()
        return len(records)
    except Exception as e:
        logger.warning(f"backfill {symbol} {name}: {e}")
        return 0


async def run_backfill():
    sectors = await fetch_sectors()
    logger.info(f"Found {len(sectors)} sectors")
    total = 0
    for symbol, name in sectors[:10]:  # Only backfill first 10 for speed
        n = await backfill_sector(symbol, name)
        total += n
        logger.info(f"{symbol} {name}: {n} rows")
    logger.info(f"Backfill done: {total} total rows (10 sectors)")


if __name__ == "__main__":
    asyncio.run(run_backfill())
