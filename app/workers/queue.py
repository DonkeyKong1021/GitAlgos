import json
from typing import Any, Dict

import redis

from app.settings import settings


class TaskQueue:
    def __init__(self) -> None:
        self.client = redis.from_url(settings.redis_url)
        self.channel = "tasks"

    def publish(self, message: Dict[str, Any]) -> None:
        self.client.lpush(self.channel, json.dumps(message))

    def pop(self) -> Dict[str, Any] | None:
        data = self.client.rpop(self.channel)
        if not data:
            return None
        return json.loads(data)
