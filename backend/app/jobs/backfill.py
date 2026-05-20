"""历史数据回填脚本 — 手动执行一次"""
import asyncio
import logging
import akshare as ak
import pandas as pd
from datetime import date, datetime, timedelta
from sqlalchemy.dialects.postgresql import insert
from app.db import async_session
from app.models.fund_flow import SectorFundFlowDaily
from app.models.sector import Sector

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SECTOR_SYMBOLS = ["BK0890", "BK0891", "BK0892", "BK0893", "BK0894", "BK0895",
                  "BK0896", "BK0897", "BK0898", "BK0899", "BK0900", "BK0901",
                  "BK0902", "BK0903", "BK0904", "BK0905", "BK0906", "BK0907",
                  "BK0908", "BK0909", "BK0910", "BK0911", "BK0912", "BK0913",
                  "BK0914", "BK0915", "BK0916", "BK0917", "BK0918", "BK0919"]

async def backfill_sector(symbol: str, start_date: str = "20250101"):
    try:
        df = await asyncio.to_thread(ak.stock_sector_fund_flow_hist, symbol=symbol)
        if df is None or df.empty:
            return 0
        col_map = {"日期": "trade_date", "主力净流入-净额": "main_net_inflow",
                   "主力净流入-净占比": "main_net_ratio", "超大单净流入-净额": "super_large_net",
                   "大单净流入-净额": "large_net", "中单净流入-净额": "medium_net",
                   "小单净流入-净额": "small_net", "成交额": "turnover", "涨跌幅": "close_pct"}
        df = df.rename(columns={k: v for k, v in col_map.items() if k in df.columns})
        async with async_session() as sess:
            records = []
            for _, row in df.iterrows():
                td = row.get("trade_date", "")
                if isinstance(td, str):
                    td = datetime.strptime(td, "%Y-%m-%d").date()
                elif hasattr(td, "date"):
                    td = td.date()
                if not isinstance(td, date) or td < date.fromisoformat(start_date[:4]+"-"+start_date[4:6]+"-"+start_date[6:]):
                    continue
                rec = {"trade_date": td, "sector_code": symbol, "data_source": "akshare"}
                for col in ["main_net_inflow", "main_net_ratio", "super_large_net",
                           "large_net", "medium_net", "small_net", "turnover", "close_pct"]:
                    if col in df.columns:
                        rec[col] = float(row[col]) if pd.notna(row[col]) else 0
                records.append(rec)
            if records:
                stmt = insert(SectorFundFlowDaily).values(records)
                stmt = stmt.on_conflict_do_update(
                    index_elements=["trade_date", "sector_code"],
                    set_={c: stmt.excluded[c] for c in ["main_net_inflow", "main_net_ratio",
                           "super_large_net", "large_net", "medium_net", "small_net", "turnover",
                           "close_pct", "data_source"]})
                await sess.execute(stmt)
                await sess.commit()
            return len(records)
    except Exception as e:
        logger.warning(f"backfill {symbol}: {e}")
        return 0

async def run_backfill():
    total = 0
    for sym in SECTOR_SYMBOLS:
        n = await backfill_sector(sym)
        total += n
        logger.info(f"{sym}: {n} rows")
    logger.info(f"Backfill done: {total} total rows")

if __name__ == "__main__":
    asyncio.run(run_backfill())
