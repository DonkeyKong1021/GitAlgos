from typing import List, Optional

from sqlalchemy.orm import Session

from app.db import models


def create_backtest(db: Session, backtest: models.BacktestRun) -> models.BacktestRun:
    db.add(backtest)
    db.commit()
    db.refresh(backtest)
    return backtest


def update_backtest(db: Session, backtest: models.BacktestRun, data: dict) -> models.BacktestRun:
    for key, value in data.items():
        setattr(backtest, key, value)
    db.add(backtest)
    db.commit()
    db.refresh(backtest)
    return backtest


def get_backtest(db: Session, backtest_id: int, owner_id: Optional[int] = None) -> Optional[models.BacktestRun]:
    query = db.query(models.BacktestRun).filter(models.BacktestRun.id == backtest_id)
    if owner_id:
        query = query.filter(models.BacktestRun.owner_id == owner_id)
    return query.first()


def list_backtests(db: Session, owner_id: Optional[int] = None) -> List[models.BacktestRun]:
    query = db.query(models.BacktestRun)
    if owner_id:
        query = query.filter(models.BacktestRun.owner_id == owner_id)
    return query.order_by(models.BacktestRun.started_at.desc()).all()
