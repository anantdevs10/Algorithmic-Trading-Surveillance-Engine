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

class BacktestResult(Base):
    __tablename__ = "backtest_results"
    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String)
    strategy_config = Column(String)  # store as JSON string
    return_pct = Column(Float)
    win_rate = Column(Float)
    max_drawdown = Column(Float)
    created_at = Column(DateTime)

class PaperOrder(Base):
    __tablename__ = "paper_orders"
    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String)
    side = Column(String)     # "buy" / "sell"
    quantity = Column(Float)
    fill_price = Column(Float)
    timestamp = Column(DateTime)

class PaperPosition(Base):
    __tablename__ = "paper_positions"
    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String, unique=True)
    quantity = Column(Float)
    avg_price = Column(Float)

class OrderEvent(Base):
    __tablename__ = "order_events"
    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String)
    side = Column(String)
    price = Column(Float)
    quantity = Column(Float)
    event_type = Column(String)  # "new" / "cancel" / "fill"
    timestamp = Column(DateTime)

class Alert(Base):
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String)
    rule_flags = Column(String)   # JSON list of triggered rule names
    anomaly_score = Column(Float, default=0.0)
    severity = Column(String)     # "low" / "medium" / "high" / "critical"
    timestamp = Column(DateTime)

'''
CREATING TWO TABLES using the parent classes using SQLAlchemy
Symbol Table --> Stores assets and stock identifiers, id, ticker(eg MICROSOFT = MSFT), name of company
Market Table --> Stores time-series price data
'''