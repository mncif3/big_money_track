import hashlib
import json
import logging
from datetime import date
from sqlalchemy import select, func
from app.db import async_session
from app.models.north import NorthCapitalDaily
from app.models.alert import Alert

logger = logging.getLogger(__name__)

async def evaluate_alerts():
    alerts_triggered = []
    # Check north capital outflow
    async with async_session() as sess:
        stmt = select(NorthCapitalDaily).order_by(NorthCapitalDaily.trade_date.desc()).limit(1)
        latest = (await sess.execute(stmt)).scalar_one_or_none()
        if latest:
            total = float(latest.total_net_inflow or 0)
            if total < -100e8:  # 100亿 outflow
                alerts_triggered.append(dict(level=1, category="north", title=f"北向资金单日大幅流出 {total/1e8:.1f}亿"))
    for a in alerts_triggered:
        key = hashlib.md5(json.dumps(a, sort_keys=True).encode()).hexdigest()
        async with async_session() as sess:
            exists = await sess.execute(select(Alert).where(Alert.detail["hash_key"].astext == key).limit(1))
            if not exists.scalar_one_or_none():
                alert = Alert(level=a["level"], category=a["category"], title=a["title"],
                              detail={"hash_key": key})
                sess.add(alert)
                await sess.commit()
    return len(alerts_triggered)
