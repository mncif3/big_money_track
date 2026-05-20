from sqlalchemy import Column, String, Integer, Text, DateTime
from sqlalchemy.dialects.postgresql import BIGINT
from app.db import Base
from datetime import datetime

class EtlJobLog(Base):
    __tablename__ = "etl_job_log"
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    job_name = Column(String(64), nullable=False)
    start_time = Column(DateTime(timezone=True), default=datetime.now)
    end_time = Column(DateTime(timezone=True))
    status = Column(String(16))
    rows_processed = Column(Integer)
    error_msg = Column(Text)
    data_source_used = Column(String(16))
