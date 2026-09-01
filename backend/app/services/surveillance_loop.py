import asyncio
import json
from datetime import datetime
import pandas as pd

from ..database import SessionLocal
from ..models import MarketData, OrderEvent, Alert, Symbol
from .detectors import (
    detect_volume_spike,
    detect_price_velocity,
    detect_volume_price_divergence,
    detect_time_of_day_anomaly,
    detect_spoofing,
    detect_wash_trading,
)

CHECK_INTERVAL_SECONDS = 15

async def run_surveillance_loop(broadcast_fn):
    """Runs forever in the background. Every CHECK_INTERVAL_SECONDS, evaluates
    every symbol against all 6 detection rules and, if any fire, inserts an
    Alert row and pushes it to connected clients over the /ws/alerts socket."""
    while True:
        db = SessionLocal()
        try:
            symbols = db.query(Symbol).all()
            for sym in symbols:
                await _check_symbol(db, sym.ticker, broadcast_fn)
        finally:
            db.close()
        await asyncio.sleep(CHECK_INTERVAL_SECONDS)


async def _check_symbol(db, ticker, broadcast_fn):
    rows = (
        db.query(MarketData)
        .filter(MarketData.ticker == ticker)
        .order_by(MarketData.timestamp)
        .all()
    )
    if len(rows) < 30:
        return  # not enough history for rolling windows yet

    df = pd.DataFrame([{
        "timestamp": r.timestamp, "close": r.close, "volume": r.volume,
    } for r in rows])

    flags = []
    if detect_volume_spike(df).iloc[-1]:
        flags.append("volume_spike")
    if detect_price_velocity(df).iloc[-1]:
        flags.append("price_velocity")
    if detect_volume_price_divergence(df).iloc[-1]:
        flags.append("volume_price_divergence")
    if detect_time_of_day_anomaly(df).iloc[-1]:
        flags.append("time_of_day_anomaly")

    order_rows = (
        db.query(OrderEvent)
        .filter(OrderEvent.ticker == ticker)
        .order_by(OrderEvent.timestamp)
        .all()
    )
    if order_rows:
        odf = pd.DataFrame([{
            "timestamp": o.timestamp, "event_type": o.event_type,
            "side": o.side, "quantity": o.quantity,
        } for o in order_rows])
        try:
            if detect_spoofing(odf).iloc[-1]:
                flags.append("spoofing")
        except Exception:
            pass
        try:
            if detect_wash_trading(odf).iloc[-1]:
                flags.append("wash_trading")
        except Exception:
            pass

    if not flags:
        return

    severity = "critical" if len(flags) >= 3 else "high" if len(flags) == 2 else "medium"

    alert = Alert(
        ticker=ticker,
        rule_flags=json.dumps(flags),
        anomaly_score=0.0,
        severity=severity,
        timestamp=datetime.now(),
    )
    db.add(alert)
    db.commit()
    db.refresh(alert)

    await broadcast_fn({
        "id": alert.id, "ticker": alert.ticker, "rule_flags": flags,
        "severity": alert.severity, "timestamp": str(alert.timestamp),
    })