"""Simple SMA crossover strategy producing long signals."""

from typing import Dict
import pandas as pd


def strategy_config() -> Dict:
    return {
        "name": "SMA Crossover",
        "params": {"fast": 10, "slow": 30},
        "assets": ["AAPL"],
        "timeframe": "1d",
    }


def generate_signals(data: pd.DataFrame, params: Dict) -> pd.Series:
    fast = int(params.get("fast", 10))
    slow = int(params.get("slow", 30))
    fast_ma = data["close"].rolling(fast).mean()
    slow_ma = data["close"].rolling(slow).mean()
    signal = (fast_ma > slow_ma).astype(int)
    return signal.fillna(0)
