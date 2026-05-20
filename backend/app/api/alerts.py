from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.api.deps import get_db
from app.models.alert import Alert

router = APIRouter(prefix="/api/alerts", tags=["alerts"])

@router.get("")
async def list_alerts(level: int = Query(None), limit: int = Query(50), db: AsyncSession = Depends(get_db)):
    stmt = select(Alert).order_by(desc(Alert.alert_time)).limit(limit)
    if level:
        stmt = stmt.where(Alert.level == level)
    rows = (await db.execute(stmt)).scalars().all()
    return [{"id": r.id, "alert_time": str(r.alert_time), "level": r.level,
             "category": r.category, "title": r.title, "pushed": r.pushed} for r in rows]
