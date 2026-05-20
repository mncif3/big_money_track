from sqlalchemy import Column, String, Numeric, Date, DateTime
from app.db import Base
from datetime import datetime

class SectorFundFlowDaily(Base):
    __tablename__ = "sector_fund_flow_daily"
    trade_date = Column(Date, primary_key=True)
    sector_code = Column(String(20), primary_key=True)
    close_pct = Column(Numeric(8, 4))
    main_net_inflow = Column(Numeric(18, 2))
    main_net_ratio = Column(Numeric(8, 4))
    super_large_net = Column(Numeric(18, 2))
    large_net = Column(Numeric(18, 2))
    medium_net = Column(Numeric(18, 2))
    small_net = Column(Numeric(18, 2))
    turnover = Column(Numeric(18, 2))
    leader_stock = Column(String(10))
    leader_pct = Column(Numeric(8, 4))
    data_source = Column(String(16), default="akshare")
    created_at = Column(DateTime(timezone=True), default=datetime.now)

class StockFundFlowDaily(Base):
    __tablename__ = "stock_fund_flow_daily"
    trade_date = Column(Date, primary_key=True)
    stock_code = Column(String(10), primary_key=True)
    close_price = Column(Numeric(12, 3))
    close_pct = Column(Numeric(8, 4))
    main_net_inflow = Column(Numeric(18, 2))
    main_net_ratio = Column(Numeric(8, 4))
    super_large_net = Column(Numeric(18, 2))
    large_net = Column(Numeric(18, 2))
    medium_net = Column(Numeric(18, 2))
    small_net = Column(Numeric(18, 2))
    turnover = Column(Numeric(18, 2))
    turnover_rate = Column(Numeric(8, 4))

class SectorFundFlowIntraday(Base):
    __tablename__ = "sector_fund_flow_intraday"
    snapshot_time = Column(DateTime(timezone=True), primary_key=True)
    sector_code = Column(String(20), primary_key=True)
    main_net_inflow = Column(Numeric(18, 2))
    turnover = Column(Numeric(18, 2))
    close_pct = Column(Numeric(8, 4))
