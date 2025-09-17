from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd

from app.backtest.metrics import compute_basic_metrics, save_quantstats_report
from app.backtest.plots import save_equity_curve
from app.settings import settings
from app.strategies.sandbox import run_strategy
from app.strategies.registry import list_example_strategies


@dataclass
class BacktestResult:
    equity_curve: pd.Series
    trades: List[Dict]
    metrics: Dict[str, float]
    equity_path: Path
    report_path: Path


class SimpleBacktraderEngine:
    def __init__(self, storage_dir: Path) -> None:
        self.storage_dir = storage_dir
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def _load_strategy(self, code: str):
        context: Dict[str, object] = {}
        locals_result = run_strategy(code, context)
        if "generate_signals" not in locals_result:
            raise ValueError("Strategy must define generate_signals(data, params)")
        return locals_result["generate_signals"]

    def run(
        self,
        *,
        code: str,
        params: Dict,
        data: pd.DataFrame,
        initial_cash: float = 100_000,
        run_id: int = 0,
    ) -> BacktestResult:
        strategy_fn = self._load_strategy(code)
        signal = strategy_fn(data, params)
        signal = signal.reindex(data.index).fillna(0)
        returns = data["close"].pct_change().fillna(0)
        positions = signal.shift(1).fillna(0)
        pnl = positions * returns
        equity_curve = (1 + pnl).cumprod() * initial_cash
        metrics = compute_basic_metrics(equity_curve)
        trades: List[Dict] = []
        for idx in range(1, len(signal)):
            if signal.iloc[idx] != signal.iloc[idx - 1]:
                trades.append(
                    {
                        "timestamp": data.index[idx].isoformat() if isinstance(data.index[idx], datetime) else str(data.index[idx]),
                        "side": "buy" if signal.iloc[idx] > signal.iloc[idx - 1] else "sell",
                        "price": float(data["close"].iloc[idx]),
                        "qty": float(signal.iloc[idx]),
                    }
                )
        equity_path = save_equity_curve(equity_curve, self.storage_dir / f"equity_{run_id}.png")
        report_path = save_quantstats_report(equity_curve, run_id, self.storage_dir / "reports")
        return BacktestResult(
            equity_curve=equity_curve,
            trades=trades,
            metrics=metrics,
            equity_path=equity_path,
            report_path=report_path,
        )


def get_engine() -> SimpleBacktraderEngine:
    storage = Path(__file__).resolve().parent.parent / "storage"
    return SimpleBacktraderEngine(storage)
