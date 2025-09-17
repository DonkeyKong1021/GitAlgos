from typing import List, Optional

from sqlalchemy.orm import Session

from app.db import models


def create_strategy(
    db: Session,
    *,
    owner_id: int,
    name: str,
    description: str,
    code: str,
    params: dict,
    assets: List[str],
    timeframe: str,
) -> models.Strategy:
    strategy = models.Strategy(
        owner_id=owner_id,
        name=name,
        description=description,
        code=code,
        params=params,
        assets=assets,
        timeframe=timeframe,
    )
    db.add(strategy)
    db.commit()
    db.refresh(strategy)
    return strategy


def get_strategy(db: Session, strategy_id: int, owner_id: Optional[int] = None) -> Optional[models.Strategy]:
    query = db.query(models.Strategy).filter(models.Strategy.id == strategy_id)
    if owner_id:
        query = query.filter(models.Strategy.owner_id == owner_id)
    return query.first()


def list_strategies(db: Session, owner_id: Optional[int] = None) -> List[models.Strategy]:
    query = db.query(models.Strategy)
    if owner_id:
        query = query.filter(models.Strategy.owner_id == owner_id)
    return query.order_by(models.Strategy.created_at.desc()).all()


def update_strategy(db: Session, strategy: models.Strategy, data: dict) -> models.Strategy:
    for key, value in data.items():
        setattr(strategy, key, value)
    db.add(strategy)
    db.commit()
    db.refresh(strategy)
    return strategy


def delete_strategy(db: Session, strategy: models.Strategy) -> None:
    db.delete(strategy)
    db.commit()
