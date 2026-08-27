import pandas as pd
import numpy as np

def detect_volume_spike(df: pd.DataFrame, window=20, k=2.0) -> pd.Series:
    """Flag bars where volume exceeds rolling mean + k * rolling std."""
    roll_mean = df["volume"].rolling(window).mean()
    roll_std = df["volume"].rolling(window).std()
    return df["volume"] > (roll_mean + k * roll_std)

def detect_price_velocity(df: pd.DataFrame, window=5, k=3.0) -> pd.Series:
    """Flag bars where the short-term price change exceeds k rolling-return std devs."""
    returns = df["close"].pct_change()
    velocity = df["close"].diff(window)
    threshold = returns.rolling(window).std() * k * df["close"]
    return velocity.abs() > threshold

def detect_volume_price_divergence(df: pd.DataFrame, window=10) -> pd.Series:
    """Flag when price trend and volume trend move in opposite directions."""
    price_trend = df["close"].diff(window)
    volume_trend = df["volume"].diff(window)
    return (price_trend * volume_trend) < 0  # opposite signs

def detect_time_of_day_anomaly(df: pd.DataFrame, k=2.5) -> pd.Series:
    """Flag activity that's unusual for that specific hour, vs. the symbol's own history."""
    df = df.copy()
    df["hour"] = pd.to_datetime(df["timestamp"]).dt.hour
    hourly_mean = df.groupby("hour")["volume"].transform("mean")
    hourly_std = df.groupby("hour")["volume"].transform("std")
    return df["volume"] > (hourly_mean + k * hourly_std)

def detect_spoofing(order_events: pd.DataFrame, window="30s", k=3.0) -> pd.Series:
    """Flag windows with an abnormally high order placement-to-cancellation rate."""
    order_events = order_events.set_index("timestamp").sort_index()
    is_cancel = (order_events["event_type"] == "cancel").astype(int)
    cancel_rate = is_cancel.rolling(window).mean()
    threshold = cancel_rate.rolling(window).mean() + k * cancel_rate.rolling(window).std()
    return cancel_rate > threshold

def detect_wash_trading(trades: pd.DataFrame, window="30s") -> pd.Series:
    """Flag windows where matched buy/sell volume between correlated accounts is high."""
    buys = trades[trades["side"] == "buy"].set_index("timestamp")["quantity"]
    sells = trades[trades["side"] == "sell"].set_index("timestamp")["quantity"]
    buy_roll = buys.rolling(window).sum()
    sell_roll = sells.rolling(window).sum()
    matched = pd.concat([buy_roll, sell_roll], axis=1).min(axis=1)
    return matched > matched.rolling(window).mean() + 2 * matched.rolling(window).std()