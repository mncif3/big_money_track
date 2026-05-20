from sqlalchemy import Column, String, SmallInteger, Numeric, Date, DateTime
from app.db import Base
from datetime import datetime

class SouthCapitalDaily(Base):
    __tablename__ = "south_capital_daily"
    trade_date = Column(Date, primary_key=True)
    sh_net_inflow = Column(Numeric(18, 2))
    sz_net_inflow = Column(Numeric(18, 2))
    total_net_inflow = Column(Numeric(18, 2))
    sh_turnover = Column(Numeric(18, 2))
    sz_turnover = Column(Numeric(18, 2))
    holding_value = Column(Numeric(18, 2))
    ah_premium = Column(Numeric(8, 4))
    created_at = Column(DateTime(timezone=True), default=datetime.now)

class SouthTop10Daily(Base):
    __tablename__ = "south_top10_daily"
    trade_date = Column(Date, primary_key=True)
    channel = Column(String(8), primary_key=True)
    rank = Column(SmallInteger, primary_key=True)
    stock_code = Column(String(10), nullable=False)
    buy_amount = Column(Numeric(18, 2))
    sell_amount = Column(Numeric(18, 2))
    net_amount = Column(Numeric(18, 2))
