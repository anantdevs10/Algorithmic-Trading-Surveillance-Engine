from pydantic import BaseModel
from datetime import datetime

class SymbolOut(BaseModel):
    ticker: str
    name: str
    class Config:
        from_attributes = True

#This allows Pydantic to automatically serialize database objects from ORMs like SQLAlchemy.

class MarketDataOut(BaseModel):
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int
    class Config:
        from_attributes = True



'''
two Pydantic schemas used in Web Frameworks like FastAPI to format, validate and serialize data retruned by an API
used with SQLAlchemy 
used for request/response validation and serialization.
'''