from datetime import datetime
from typing import Dict

import pandas as pd
from alpha_vantage.foreignexchange import ForeignExchange
from alpha_vantage.timeseries import TimeSeries

from app.settings import settings
from app.data.cache import cache
from app.data.rate_limit import backoff


@cache(ttl=60)
@backoff()
def fetch_fx_intraday(pair: str, interval: str = "5min") -> pd.DataFrame:
    fx = ForeignExchange(key=settings.alpha_vantage_api_key)
    data, _ = fx.get_currency_exchange_intraday(pair[:3], pair[3:], interval=interval, outputsize="compact")
    df = pd.DataFrame.from_dict(data, orient="index")
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()
    df = df.rename(columns=lambda c: c.split(". ")[-1].lower())
    df = df.astype(float)
    return df


@cache(ttl=60)
@backoff()
def fetch_equity_intraday(symbol: str, interval: str = "5min") -> pd.DataFrame:
    ts = TimeSeries(key=settings.alpha_vantage_api_key, output_format="pandas")
    data, _ = ts.get_intraday(symbol=symbol, interval=interval, outputsize="compact")
    data.index = pd.to_datetime(data.index)
    data = data.sort_index()
    data = data.rename(columns=lambda c: c.split(". ")[-1].lower())
    return data
