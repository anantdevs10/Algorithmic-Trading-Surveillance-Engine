import pandas as pd
import numpy as np

def sma_crossover_signals(df: pd.DataFrame, short_window=10, long_window=30) -> pd.DataFrame:
    df = df.copy()
    df["sma_short"] = df["close"].rolling(short_window).mean()
    df["sma_long"] = df["close"].rolling(long_window).mean()
    df["signal"] = 0
    df.loc[df["sma_short"] > df["sma_long"], "signal"] = 1   # buy
    df.loc[df["sma_short"] < df["sma_long"], "signal"] = -1  # sell
    return df

def simulate_execution(df: pd.DataFrame, starting_cash=10_000.0):
    cash = starting_cash
    position = 0
    equity_curve = []
    trades = []  # store realized P&L per closed trade

    for _, row in df.iterrows():
        price = row["close"]
        if row["signal"] == 1 and position == 0:
            position = cash / price
            entry_price = price
            cash = 0
        elif row["signal"] == -1 and position > 0:
            cash = position * price
            trades.append(price - entry_price)  # P&L per share
            position = 0
        equity_curve.append(cash + position * price)

    df["equity"] = equity_curve
    return df, trades

def compute_metrics(df: pd.DataFrame, trades: list, starting_cash=10_000.0) -> dict:
    final_equity = df["equity"].iloc[-1]
    total_return = (final_equity / starting_cash) - 1

    win_rate = (
        sum(1 for t in trades if t > 0) / len(trades) if trades else 0.0
    )

    running_max = df["equity"].cummax()
    drawdown = df["equity"] / running_max - 1
    max_drawdown = drawdown.min()

    return {
        "return": round(total_return, 4),
        "win_rate": round(win_rate, 4),
        "max_drawdown": round(max_drawdown, 4),
    }