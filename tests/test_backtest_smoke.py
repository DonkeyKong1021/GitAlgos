import pandas as pd
import pytest


@pytest.fixture(autouse=True)
def patch_data(monkeypatch):
    def fake_fetch(symbol, start, end, timeframe="1d"):
        index = pd.date_range(start="2022-01-01", periods=30, freq="D")
        prices = pd.Series(range(30), index=index) + 100
        return pd.DataFrame({"close": prices})

    monkeypatch.setattr("app.backtest.router.fetch_history", fake_fetch)


def test_backtest_run(client):
    client.post(
        "/auth/register",
        json={"email": "bt@example.com", "password": "Password123", "role": "admin"},
    )
    login = client.post(
        "/auth/login",
        json={"email": "bt@example.com", "password": "Password123"},
    )
    token = login.json()["access_token"]
    payload = {"example": "sma_crossover", "start": "2022-01-01", "end": "2022-02-01"}
    response = client.post("/backtests/run", json=payload, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert "metrics" in data
    assert set(data["metrics"].keys()) >= {"cagr", "sharpe", "max_drawdown"}
