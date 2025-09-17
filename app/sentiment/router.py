from fastapi import APIRouter, Depends

from app.deps import get_current_user
from app.sentiment.service import get_service

router = APIRouter(prefix="/sentiment", tags=["sentiment"])


@router.get("")
def sentiment(symbol: str, user=Depends(get_current_user)):
    service = get_service()
    return service.get_sentiment(symbol)
