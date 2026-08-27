import json
from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import pandas as pd
from ..database import get_db
from ..models import MarketData, BacktestResult
from ..services.backtester import sma_crossover_signals, simulate_execution, compute_metrics

router = APIRouter(prefix="/api/backtest", tags=["backtest"])

@router.post("/")
def run_backtest(symbol: str, short_window: int = 10, long_window: int = 30,
                  db: Session = Depends(get_db)):
    rows = db.query(MarketData).filter(MarketData.ticker == symbol.upper()).all()
    df = pd.DataFrame([{"close": r.close} for r in rows])

    signaled = sma_crossover_signals(df, short_window, long_window)
    executed, trades = simulate_execution(signaled)
    metrics = compute_metrics(executed, trades)

    result = BacktestResult(
        ticker=symbol.upper(),
        strategy_config=json.dumps({"short_window": short_window, "long_window": long_window}),
        return_pct=metrics["return"], win_rate=metrics["win_rate"],
        max_drawdown=metrics["max_drawdown"], created_at=datetime.now(),
    )
    db.add(result); db.commit(); db.refresh(result)
    return {"id": result.id, **metrics}

@router.get("/{backtest_id}")
def get_backtest(backtest_id: int, db: Session = Depends(get_db)):
    return db.query(BacktestResult).filter(BacktestResult.id == backtest_id).first()