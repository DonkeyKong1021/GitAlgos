from datetime import datetime, timedelta
from typing import List


class NewsStub:
    def fetch(self, symbol: str, limit: int = 10) -> List[dict]:
        now = datetime.utcnow()
        return [
            {"title": f"{symbol} moves", "published_at": (now - timedelta(minutes=i * 30)).isoformat()}
            for i in range(limit)
        ]
