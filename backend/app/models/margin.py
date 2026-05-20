from sqlalchemy import Column, Numeric, Date, DateTime
from app.db import Base
from datetime import datetime

class MarginDaily(Base):
    __tablename__ = "margin_daily"
    trade_date = Column(Date, primary_key=True)
    margin_balance = Column(Numeric(18, 2))
    short_balance = Column(Numeric(18, 2))
    margin_net_buy = Column(Numeric(18, 2))
    short_net_sell = Column(Numeric(18, 2))
    margin_turnover = Column(Numeric(18, 2))
    margin_ratio = Column(Numeric(8, 4))
    created_at = Column(DateTime(timezone=True), default=datetime.now)
