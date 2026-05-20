import logging
from datetime import datetime, date
from sqlalchemy.dialects.postgresql import insert
from app.db import async_session
from app.models.south import SouthCapitalDaily
from app.models.etl_log import EtlJobLog
from app.datasource import data_source_mgr

logger = logging.getLogger(__name__)

async def daily_south_summary_job():
    async with async_session() as sess:
        job_log = EtlJobLog(job_name="daily_south_summary", status="running")
        sess.add(job_log); await sess.commit()
        try:
            data_source_mgr.init_default()
            df, src = await data_source_mgr.call("fetch_south_summary")
            today = date.today()
            rec = {"trade_date": today}
            if not df.empty:
                row = df.iloc[-1]
                rec.update({k: float(row.get(k, 0) or 0) for k in ["sh_net_inflow", "sz_net_inflow", "total_net_inflow"] if k in df.columns})
            stmt = insert(SouthCapitalDaily).values(**rec).on_conflict_do_update(
                index_elements=["trade_date"], set_={k: stmt.excluded[k] for k in rec if k != "trade_date"})
            await sess.execute(stmt)
            job_log.status = "success"; job_log.data_source_used = src
        except Exception as e:
            job_log.status = "failed"; job_log.error_msg = str(e)
        job_log.end_time = datetime.now(); await sess.commit()
