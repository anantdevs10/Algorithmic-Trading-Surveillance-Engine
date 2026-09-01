import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib

def build_trader_features(order_events: pd.DataFrame) -> pd.DataFrame:
    """One row per trader: order-to-trade ratio, cancellation rate,
    inter-arrival time, order-size clustering."""
    grouped = order_events.groupby("trader_id")
    features = pd.DataFrame({
        "order_to_trade_ratio": grouped.apply(
            lambda g: (g["event_type"] == "new").sum() / max((g["event_type"] == "fill").sum(), 1)
        ),
        "cancellation_rate": grouped.apply(
            lambda g: (g["event_type"] == "cancel").mean()
        ),
        "inter_arrival_time": grouped.apply(
            lambda g: g["timestamp"].sort_values().diff().dt.total_seconds().mean()
        ),
        "order_size_std": grouped["quantity"].std(),
    }).fillna(0)
    return features

def train_isolation_forest(features: pd.DataFrame, contamination=0.02):
    model = IsolationForest(contamination=contamination, random_state=42)
    model.fit(features)
    scores = model.decision_function(features)  # lower = more anomalous
    joblib.dump(model, "app/ml/isolation_forest.pkl")
    return model, scores
def combine_severity(rule_flags: list[str], anomaly_score: float, score_min: float, score_max: float) -> str:
    normalized = (anomaly_score - score_min) / (score_max - score_min + 1e-9)
    inverted = 1 - normalized  # lower raw score = more anomalous = higher severity
    rule_weight = len(rule_flags) / 6  # 6 total rules from Phase 6

    combined = 0.5 * inverted + 0.5 * rule_weight
    if combined > 0.75 and len(rule_flags) > 0:
        return "critical"
    if combined > 0.5:
        return "high"
    if combined > 0.25:
        return "medium"
    return "low"