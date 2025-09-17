from collections import deque
from typing import Deque, Dict, List

from app.sentiment.news_stub import NewsStub
from app.sentiment.vader_provider import score_texts


class SentimentService:
    def __init__(self, window: int = 20) -> None:
        self.window = window
        self.history: Dict[str, Deque[float]] = {}
        self.news = NewsStub()

    def get_sentiment(self, symbol: str) -> Dict[str, object]:
        items = self.news.fetch(symbol)
        texts = [item["title"] for item in items]
        score = score_texts(texts)
        buffer = self.history.setdefault(symbol, deque(maxlen=self.window))
        buffer.append(score)
        rolling = sum(buffer) / len(buffer)
        return {"symbol": symbol, "score": score, "rolling_score": rolling, "items": items[:5]}


def get_service() -> SentimentService:
    return SentimentService()
