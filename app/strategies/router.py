from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.deps import get_current_user
from app.db import models
from app.db.crud import strategies as strategies_crud
from app.db.session import get_db
from app.strategies import schemas
from app.strategies.registry import list_example_strategies

router = APIRouter(prefix="/strategies", tags=["strategies"])


@router.get("/examples")
def get_examples():
    return list_example_strategies()


@router.post("", response_model=schemas.StrategyRead)
def create_strategy(
    payload: schemas.StrategyCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    strategy = strategies_crud.create_strategy(
        db,
        owner_id=current_user.id,
        name=payload.name,
        description=payload.description or "",
        code=payload.code,
        params=payload.params,
        assets=payload.assets,
        timeframe=payload.timeframe,
    )
    return strategy


@router.get("", response_model=list[schemas.StrategyRead])
def list_strategies(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return strategies_crud.list_strategies(db, owner_id=current_user.id)


@router.get("/{strategy_id}", response_model=schemas.StrategyRead)
def get_strategy(strategy_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    strategy = strategies_crud.get_strategy(db, strategy_id, owner_id=current_user.id)
    if not strategy:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Strategy not found")
    return strategy


@router.put("/{strategy_id}", response_model=schemas.StrategyRead)
def update_strategy(
    strategy_id: int,
    payload: schemas.StrategyUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    strategy = strategies_crud.get_strategy(db, strategy_id, owner_id=current_user.id)
    if not strategy:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Strategy not found")
    updated = strategies_crud.update_strategy(db, strategy, {k: v for k, v in payload.dict(exclude_unset=True).items()})
    return updated


@router.delete("/{strategy_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_strategy(strategy_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    strategy = strategies_crud.get_strategy(db, strategy_id, owner_id=current_user.id)
    if not strategy:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Strategy not found")
    strategies_crud.delete_strategy(db, strategy)
    return {}
