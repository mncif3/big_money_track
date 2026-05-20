from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, func
from app.api.deps import get_db
from app.models.etl_log import EtlJobLog

router = APIRouter(prefix="/api/system", tags=["system"])

@router.get("/etl-status")
async def etl_status(db: AsyncSession = Depends(get_db)):
    subq = (
        select(EtlJobLog.job_name, func.max(EtlJobLog.start_time).label("last_start"))
        .group_by(EtlJobLog.job_name).subquery()
    )
    stmt = select(EtlJobLog).join(subq, (EtlJobLog.job_name == subq.c.job_name) & (EtlJobLog.start_time == subq.c.last_start))
    rows = (await db.execute(stmt)).scalars().all()
    return [{"job_name": r.job_name, "status": r.status, "start_time": str(r.start_time),
             "end_time": str(r.end_time) if r.end_time else None, "rows_processed": r.rows_processed}
            for r in rows]
