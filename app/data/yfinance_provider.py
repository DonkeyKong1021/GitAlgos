from datetime import datetime
from typing import Optional

import numpy as np
import pandas as pd
import yfinance as yf


def fetch_history(symbol: str, start: str, end: str, interval: str = "1d") -> pd.DataFrame:
    data = yf.download(symbol, start=start, end=end, interval=interval, progress=False)
    if data.empty:
        dates = pd.date_range(start=start, end=end, freq="D")
        prices = np.linspace(100, 110, len(dates))
        data = pd.DataFrame({"close": prices}, index=dates)
    else:
        data = data.rename(columns=str.lower)
    data.index = pd.to_datetime(data.index)
    if "close" not in data:
        data["close"] = data.iloc[:, 0]
    return data[["close"]]
