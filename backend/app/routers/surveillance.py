from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import pandas as pd
from ..database import get_db
from ..models import OrderEvent
from ..services.ml_model import build_trader_features, train_isolation_forest

router = APIRouter(prefix="/api/surveillance", tags=["surveillance"])

RULE_CONFIG = {"volume_spike_k": 2.0, "price_velocity_k": 3.0}  # in-memory for now

@router.post("/rules/")
def update_rules(volume_spike_k: float, price_velocity_k: float):
    RULE_CONFIG["volume_spike_k"] = volume_spike_k
    RULE_CONFIG["price_velocity_k"] = price_velocity_k
    return RULE_CONFIG

@router.post("/model/retrain/")
def retrain_model(db: Session = Depends(get_db)):
    events = pd.DataFrame([e.__dict__ for e in db.query(OrderEvent).all()])
    features = build_trader_features(events)
    _, scores = train_isolation_forest(features)
    return {"status": "retrained", "traders_scored": len(scores)}