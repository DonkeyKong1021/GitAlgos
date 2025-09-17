from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd


def compute_basic_metrics(equity_curve: pd.Series) -> Dict[str, float]:
    returns = equity_curve.pct_change().dropna()
    if returns.empty:
        return {"cagr": 0.0, "sharpe": 0.0, "max_drawdown": 0.0}
    total_return = equity_curve.iloc[-1] / equity_curve.iloc[0] - 1
    years = len(returns) / 252
    cagr = (1 + total_return) ** (1 / max(years, 1e-6)) - 1
    sharpe = np.sqrt(252) * returns.mean() / (returns.std() + 1e-9)
    running_max = equity_curve.cummax()
    drawdown = (equity_curve - running_max) / running_max
    max_drawdown = drawdown.min()
    return {"cagr": float(cagr), "sharpe": float(sharpe), "max_drawdown": float(max_drawdown)}


def save_quantstats_report(equity_curve: pd.Series, run_id: int, storage_dir: Path) -> Path:
    storage_dir.mkdir(parents=True, exist_ok=True)
    path = storage_dir / f"{run_id}.html"
    html = f"<html><body><h1>Backtest Report {run_id}</h1><p>Points: {len(equity_curve)}</p></body></html>"
    path.write_text(html)
    return path
