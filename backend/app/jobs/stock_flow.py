import logging
from datetime import datetime, date
import pandas as pd
from sqlalchemy.dialects.postgresql import insert
from app.db import async_session
from app.models.fund_flow import StockFundFlowDaily
from app.models.etl_log import EtlJobLog
from app.datasource import data_source_mgr

logger = logging.getLogger(__name__)

async def daily_stock_flow_job():
    async with async_session() as sess:
        job_log = EtlJobLog(job_name="daily_stock_flow", status="running")
        sess.add(job_log); await sess.commit()
        try:
            data_source_mgr.init_default()
            df, src = await data_source_mgr.call("fetch_stock_flow", indicator="今日")
            col_map = {"股票代码": "stock_code", "最新价": "close_price",
                       "今日涨跌幅": "close_pct", "今日主力净流入-净额": "main_net_inflow",
                       "今日主力净流入-净占比": "main_net_ratio",
                       "今日超大单净流入-净额": "super_large_net",
                       "今日大单净流入-净额": "large_net",
                       "今日中单净流入-净额": "medium_net",
                       "今日小单净流入-净额": "small_net",
                       "今日成交额": "turnover", "今日换手率": "turnover_rate"}
            df = df.rename(columns={k: v for k, v in col_map.items() if k in df.columns})
            today = date.today()
            records = []
            for _, row in df.iterrows():
                rec = {"trade_date": today, "stock_code": str(row.get("stock_code", ""))}
                for col in ["close_price", "close_pct", "main_net_inflow", "main_net_ratio",
                           "super_large_net", "large_net", "medium_net", "small_net",
                           "turnover", "turnover_rate"]:
                    if col in df.columns:
                        rec[col] = float(row[col]) if pd.notna(row[col]) else 0
                records.append(rec)
            stmt = insert(StockFundFlowDaily).values(records)
            stmt = stmt.on_conflict_do_update(
                index_elements=["trade_date", "stock_code"],
                set_={c.name: stmt.excluded[c.name] for c in StockFundFlowDaily.__table__.columns
                      if c.name not in ("trade_date", "stock_code")})
            await sess.execute(stmt)
            job_log.status = "success"; job_log.rows_processed = len(records)
            job_log.data_source_used = src
        except Exception as e:
            job_log.status = "failed"; job_log.error_msg = str(e)
            logger.error(f"daily_stock_flow: {e}")
        job_log.end_time = datetime.now(); await sess.commit()
