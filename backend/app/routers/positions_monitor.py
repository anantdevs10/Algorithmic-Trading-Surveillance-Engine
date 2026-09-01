from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import OrderEvent
from ..services.detectors import detect_spoofing
import pandas as pd

router = APIRouter(prefix="/api/positions", tags=["positions"])

@router.get("/monitor/{trader_id}")
def monitor_trader(trader_id: str, db: Session = Depends(get_db)):
    events = db.query(OrderEvent).filter(OrderEvent.trader_id == trader_id).all()
    df = pd.DataFrame([e.__dict__ for e in events])
    if df.empty:
        return {"trader_id": trader_id, "flags": []}
    flagged = detect_spoofing(df)
    return {"trader_id": trader_id, "flags": df[flagged].to_dict("records")}