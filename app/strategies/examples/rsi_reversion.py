"""RSI mean reversion returning long-only exposures."""

from typing import Dict
import pandas as pd


def strategy_config() -> Dict:
    return {
        "name": "RSI Reversion",
        "params": {"period": 14, "lower": 30, "upper": 70},
        "assets": ["EURUSD=X"],
        "timeframe": "1h",
    }


def generate_signals(data: pd.DataFrame, params: Dict) -> pd.Series:
    period = int(params.get("period", 14))
    lower = float(params.get("lower", 30))
    upper = float(params.get("upper", 70))
    delta = data["close"].diff()
    gain = delta.clip(lower=0).rolling(period).mean()
    loss = (-delta.clip(upper=0)).rolling(period).mean()
    rs = gain / (loss.replace(0, 1e-9))
    rsi = 100 - (100 / (1 + rs))
    signal = pd.Series(0, index=data.index)
    signal[rsi < lower] = 1
    signal[rsi > upper] = 0
    return signal.ffill().fillna(0)
