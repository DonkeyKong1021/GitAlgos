from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends

from app.data.alpha_vantage_provider import fetch_equity_intraday, fetch_fx_intraday
from app.data.yfinance_provider import fetch_history
from app.deps import get_current_user

router = APIRouter(prefix="/data", tags=["data"])


@router.get("/history")
def history(symbol: str, start: str, end: Optional[str] = None, timeframe: str = "1d", user=Depends(get_current_user)):
    df = fetch_history(symbol, start, end or datetime.utcnow().date().isoformat(), timeframe)
    return df.reset_index().to_dict(orient="records")


@router.get("/intraday/equity")
def intraday_equity(symbol: str, interval: str = "5min", user=Depends(get_current_user)):
    df = fetch_equity_intraday(symbol, interval)
    return df.reset_index().to_dict(orient="records")


@router.get("/intraday/fx")
def intraday_fx(pair: str, interval: str = "5min", user=Depends(get_current_user)):
    df = fetch_fx_intraday(pair, interval)
    return df.reset_index().to_dict(orient="records")
