from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import MarketData, PaperOrder, PaperPosition

router = APIRouter(prefix="/api/paper-trade", tags=["paper-trade"])

@router.post("/order/")
def submit_order(symbol: str, side: str, quantity: float, db: Session = Depends(get_db)):
    latest = (
        db.query(MarketData)
        .filter(MarketData.ticker == symbol.upper())
        .order_by(MarketData.timestamp.desc())
        .first()
    )
    fill_price = latest.close

    order = PaperOrder(ticker=symbol.upper(), side=side, quantity=quantity,
                        fill_price=fill_price, timestamp=datetime.now())
    db.add(order)

    position = db.query(PaperPosition).filter(PaperPosition.ticker == symbol.upper()).first()
    if position is None:
        position = PaperPosition(ticker=symbol.upper(), quantity=0, avg_price=0)
        db.add(position)

    if side == "buy":
        new_qty = position.quantity + quantity
        position.avg_price = (
            (position.avg_price * position.quantity + fill_price * quantity) / new_qty
            if new_qty else 0
        )
        position.quantity = new_qty
    else:  # sell
        position.quantity -= quantity

    db.commit()
    return {"filled_at": fill_price, "side": side, "quantity": quantity}

@router.get("/positions/")
def get_positions(db: Session = Depends(get_db)):
    positions = db.query(PaperPosition).all()
    out = []
    for p in positions:
        latest = (
            db.query(MarketData)
            .filter(MarketData.ticker == p.ticker)
            .order_by(MarketData.timestamp.desc())
            .first()
        )
        unrealized_pnl = (latest.close - p.avg_price) * p.quantity if latest else 0
        out.append({
            "ticker": p.ticker, "quantity": p.quantity,
            "avg_price": p.avg_price, "unrealized_pnl": unrealized_pnl,
        })
    return out