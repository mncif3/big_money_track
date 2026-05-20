from sqlalchemy import Column, String, Boolean, BigInteger, Date, DateTime
from app.db import Base
from datetime import datetime

class Stock(Base):
    __tablename__ = "stocks"
    stock_code = Column(String(10), primary_key=True)
    stock_name = Column(String(32), nullable=False)
    market = Column(String(8), nullable=False)
    list_date = Column(Date)
    total_share = Column(BigInteger)
    float_share = Column(BigInteger)
    is_st = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    updated_at = Column(DateTime(timezone=True), default=datetime.now)
