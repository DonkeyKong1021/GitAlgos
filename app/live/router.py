from fastapi import APIRouter, Depends, HTTPException

from app.deps import get_current_user
from app.live.manager import RiskLimits, get_manager

router = APIRouter(prefix="/live", tags=["live"])


@router.post("/start")
def start_live(broker: str, strategy_id: int, daily_loss_limit: float = 1000, max_position: float = 100000, current_user=Depends(get_current_user)):
    manager = get_manager()
    limits = RiskLimits(daily_loss_limit=daily_loss_limit, max_position=max_position)
    return manager.start(current_user.id, broker, strategy_id, limits)


@router.post("/stop")
def stop_live(current_user=Depends(get_current_user)):
    manager = get_manager()
    manager.stop(current_user.id)
    return {"status": "stopped"}


@router.get("/status")
def status(current_user=Depends(get_current_user)):
    manager = get_manager()
    state = manager.status(current_user.id)
    if not state:
        raise HTTPException(status_code=404, detail="Not running")
    return state


@router.post("/killswitch")
def killswitch(current_user=Depends(get_current_user)):
    manager = get_manager()
    return manager.killswitch(current_user.id)
