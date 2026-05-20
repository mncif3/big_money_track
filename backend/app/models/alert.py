from sqlalchemy import Column, String, SmallInteger, Boolean, DateTime
from sqlalchemy.dialects.postgresql import JSONB, BIGINT
from app.db import Base
from datetime import datetime

class Alert(Base):
    __tablename__ = "alerts"
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    alert_time = Column(DateTime(timezone=True), default=datetime.now)
    level = Column(SmallInteger, nullable=False)
    category = Column(String(32), nullable=False)
    title = Column(String(128), nullable=False)
    detail = Column(JSONB)
    pushed = Column(Boolean, default=False)
    pushed_at = Column(DateTime(timezone=True))
