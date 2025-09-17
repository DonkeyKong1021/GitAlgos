import functools
import time
from typing import Callable

from tenacity import retry, stop_after_attempt, wait_exponential


def backoff(max_attempts: int = 3):
    def decorator(func: Callable):
        @functools.wraps(func)
        @retry(stop=stop_after_attempt(max_attempts), wait=wait_exponential(multiplier=1, min=1, max=8))
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    return decorator
