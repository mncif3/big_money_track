from sqlalchemy import Column, String, BigInteger, Numeric, Date
from app.db import Base

class DragonTigerDaily(Base):
    __tablename__ = "dragon_tiger_daily"
    trade_date = Column(Date, primary_key=True)
    stock_code = Column(String(10), primary_key=True)
    reason = Column(String(128), primary_key=True)
    close_pct = Column(Numeric(8, 4))
    turnover = Column(Numeric(18, 2))
    net_buy = Column(Numeric(18, 2))
    inst_net_buy = Column(Numeric(18, 2))
    top5_buy = Column(Numeric(18, 2))
    top5_sell = Column(Numeric(18, 2))

class BlockTradeDaily(Base):
    __tablename__ = "block_trade_daily"
    trade_date = Column(Date, primary_key=True)
    stock_code = Column(String(10), primary_key=True)
    price = Column(Numeric(12, 3), primary_key=True)
    volume = Column(BigInteger, primary_key=True)
    amount = Column(Numeric(18, 2))
    premium_rate = Column(Numeric(8, 4))
    buyer = Column(String(128))
    seller = Column(String(128))
