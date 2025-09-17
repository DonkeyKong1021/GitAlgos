import enum


class Timeframe(str, enum.Enum):
    daily = "1d"
    hourly = "1h"
    minute = "1m"
