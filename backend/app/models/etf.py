from sqlalchemy import Column, String, Numeric, Date
from app.db import Base

class EtfFlowDaily(Base):
    __tablename__ = "etf_flow_daily"
    trade_date = Column(Date, primary_key=True)
    etf_code = Column(String(10), primary_key=True)
    etf_name = Column(String(64))
    share_change = Column(Numeric(18, 2))
    net_inflow = Column(Numeric(18, 2))
    track_index = Column(String(64))
