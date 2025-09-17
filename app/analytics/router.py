from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import models
from app.db.crud import backtests as backtests_crud
from app.db.session import get_db
from app.deps import get_current_user

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/summary")
def summary(backtest_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    backtest = backtests_crud.get_backtest(db, backtest_id, owner_id=current_user.id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest.metrics or {}
