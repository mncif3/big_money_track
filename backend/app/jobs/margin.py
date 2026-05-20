import logging
import pandas as pd
from datetime import datetime, date
from sqlalchemy.dialects.postgresql import insert
from app.db import async_session
from app.models.margin import MarginDaily
from app.models.etl_log import EtlJobLog
from app.datasource import data_source_mgr

logger = logging.getLogger(__name__)

async def daily_margin_job():
    async with async_session() as sess:
        job_log = EtlJobLog(job_name="daily_margin", status="running")
        sess.add(job_log); await sess.commit()
        try:
            data_source_mgr.init_default()
            df, src = await data_source_mgr.call("fetch_margin_data")
            today = date.today()
            rec = {"trade_date": today}
            if not df.empty:
                row = df.iloc[0]
                for k in ["margin_balance", "short_balance", "margin_net_buy", "margin_turnover", "margin_ratio"]:
                    if k in df.columns:
                        rec[k] = float(row[k]) if pd.notna(row[k]) else 0
            stmt = insert(MarginDaily).values(**rec)
            stmt = stmt.on_conflict_do_update(
                index_elements=["trade_date"],
                set_={c.name: stmt.excluded[c.name] for c in MarginDaily.__table__.columns
                      if c.name not in ("trade_date", "created_at")})
            await sess.execute(stmt)
            job_log.status = "success"; job_log.data_source_used = src
        except Exception as e:
            job_log.status = "failed"; job_log.error_msg = str(e)
        job_log.end_time = datetime.now(); await sess.commit()
