from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import MarketData
from ..schemas import MarketDataOut

router = APIRouter(prefix="/api/market-data", tags=["market-data"])

@router.get("/{symbol}", response_model=list[MarketDataOut]) # decorator
def get_market_data(symbol: str, db: Session = Depends(get_db)): # returns share price graph and data for specific symbol
    return (
        db.query(MarketData)
        .filter(MarketData.ticker == symbol.upper())
        .order_by(MarketData.timestamp)
        .all()
    )