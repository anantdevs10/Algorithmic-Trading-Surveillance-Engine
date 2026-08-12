from sqlalchemy import Column, Integer, String, Float, DateTime
from .database import Base

class Symbol(Base):
    __tablename__ = "symbols"
    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String, unique=True, index=True)
    name = Column(String)

class MarketData(Base):
    __tablename__ = "market_data"
    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String, index=True)
    timestamp = Column(DateTime, index=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Integer)


'''
CREATING TWO TABLES using the parent classes using SQLAlchemy
Symbol Table --> Stores assets and stock identifiers, id, ticker(eg MICROSOFT = MSFT), name of company
Market Table --> Stores time-series price data
'''