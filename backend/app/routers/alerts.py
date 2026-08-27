from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Alert

router = APIRouter(prefix="/api/alerts", tags=["alerts"])

@router.get("/")
def list_alerts(symbol: str | None = None, severity: str | None = None,
                 db: Session = Depends(get_db)):
    q = db.query(Alert)
    if symbol:
        q = q.filter(Alert.ticker == symbol.upper())
    if severity:
        q = q.filter(Alert.severity == severity)
    return q.order_by(Alert.timestamp.desc()).all()

@router.get("/{alert_id}")
def get_alert(alert_id: int, db: Session = Depends(get_db)):
    return db.query(Alert).filter(Alert.id == alert_id).first()