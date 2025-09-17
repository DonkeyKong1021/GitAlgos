from datetime import datetime
from pathlib import Path
from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.backtest.engine_bt import get_engine
from app.data.yfinance_provider import fetch_history
from app.db import models
from app.db.crud import backtests as backtests_crud
from app.db.crud import strategies as strategies_crud
from app.db.session import get_db
from app.deps import get_current_user
from app.strategies.registry import list_example_strategies

router = APIRouter(prefix="/backtests", tags=["backtests"])


@router.post("/run")
def run_backtest(
    payload: Dict[str, Any],
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    params: Dict[str, Any] = payload.get("params", {})
    strategy_code: str
    if "strategy_code" in payload:
        strategy_code = payload["strategy_code"]
    elif "strategy_id" in payload:
        strategy = strategies_crud.get_strategy(db, payload["strategy_id"], owner_id=current_user.id)
        if not strategy:
            raise HTTPException(status_code=404, detail="Strategy not found")
        strategy_code = strategy.code
        params = strategy.params or params
    else:
        examples = list_example_strategies()
        example_key = payload.get("example", "sma_crossover")
        if example_key not in examples:
            raise HTTPException(status_code=404, detail="Example strategy not found")
        strategy_code = examples[example_key]

    symbol = payload.get("symbol") or payload.get("assets", ["SPY"])[0]
    start = payload.get("start", "2022-01-01")
    end = payload.get("end", datetime.utcnow().date().isoformat())
    timeframe = payload.get("timeframe", "1d")
    data = fetch_history(symbol, start, end, timeframe)
    engine = get_engine()
    run_id = int(datetime.utcnow().timestamp())
    result = engine.run(code=strategy_code, params=params, data=data, run_id=run_id)

    backtest = models.BacktestRun(
        owner_id=current_user.id,
        strategy_id=payload.get("strategy_id"),
        status=models.BacktestStatus.completed.value,
        started_at=datetime.utcnow(),
        finished_at=datetime.utcnow(),
        settings=payload,
        metrics=result.metrics,
        equity_path=str(result.equity_path),
        report_path=str(result.report_path),
    )
    backtests_crud.create_backtest(db, backtest)
    return {
        "backtest_id": backtest.id,
        "metrics": result.metrics,
        "trades": result.trades,
        "equity_curve": result.equity_curve.tail(5).to_dict(),
    }


@router.get("/{backtest_id}")
def get_backtest(backtest_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    backtest = backtests_crud.get_backtest(db, backtest_id, owner_id=current_user.id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest


@router.get("/{backtest_id}/equity.png")
def get_equity_plot(backtest_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    backtest = backtests_crud.get_backtest(db, backtest_id, owner_id=current_user.id)
    if not backtest or not backtest.equity_path:
        raise HTTPException(status_code=404, detail="Equity curve not available")
    path = Path(backtest.equity_path)
    if not path.exists():
        raise HTTPException(status_code=404, detail="File missing")
    return FileResponse(path)


@router.get("/{backtest_id}/report")
def get_report(backtest_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    backtest = backtests_crud.get_backtest(db, backtest_id, owner_id=current_user.id)
    if not backtest or not backtest.report_path:
        raise HTTPException(status_code=404, detail="Report not available")
    path = Path(backtest.report_path)
    if not path.exists():
        raise HTTPException(status_code=404, detail="File missing")
    return FileResponse(path)
