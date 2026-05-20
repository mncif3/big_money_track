from sqlalchemy import Column, String, Boolean, Numeric, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base
from datetime import datetime

class Sector(Base):
    __tablename__ = "sectors"
    sector_code = Column(String(20), primary_key=True)
    sector_name = Column(String(64), nullable=False)
    sector_type = Column(String(16), nullable=False)
    parent_code = Column(String(20))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=datetime.now)
    updated_at = Column(DateTime(timezone=True), default=datetime.now, onupdate=datetime.now)

class StockSectorMap(Base):
    __tablename__ = "stock_sector_map"
    stock_code = Column(String(10), ForeignKey("stocks.stock_code"), primary_key=True)
    sector_code = Column(String(20), ForeignKey("sectors.sector_code"), primary_key=True)
    weight = Column(Numeric(8, 4), default=1.0)
