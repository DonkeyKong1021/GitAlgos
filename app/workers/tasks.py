import json
import time
from typing import Any, Dict

from app.backtest.engine_bt import get_engine
from app.data.yfinance_provider import fetch_history
from app.db.session import SessionLocal
from app.strategies.registry import list_example_strategies
from app.workers.queue import TaskQueue


def worker() -> None:
    queue = TaskQueue()
    while True:
        task = queue.pop()
        if not task:
            time.sleep(1)
            continue
        if task.get("type") == "backtest":
            execute_backtest(task["payload"])


def execute_backtest(payload: Dict[str, Any]) -> Dict[str, Any]:
    code = list_example_strategies()[payload.get("example", "sma_crossover")]
    data = fetch_history(payload.get("symbol", "SPY"), payload.get("start"), payload.get("end"))
    engine = get_engine()
    result = engine.run(code=code, params=payload.get("params", {}), data=data)
    with SessionLocal() as session:
        pass
    return {"metrics": result.metrics}


def seed_strategies() -> None:
    examples = list_example_strategies()
    print(json.dumps({k: v[:80] for k, v in examples.items()}, indent=2))
