import textwrap


def auth_token(client):
    client.post(
        "/auth/register",
        json={"email": "crud@example.com", "password": "Password123", "role": "admin"},
    )
    login = client.post(
        "/auth/login",
        json={"email": "crud@example.com", "password": "Password123"},
    )
    return login.json()["access_token"]


def test_strategy_crud(client):
    token = auth_token(client)
    code = """\ndef generate_signals(data, params):\n    return (data['close'] > data['close'].rolling(3).mean()).astype(int)\n"""
    create = client.post(
        "/strategies",
        json={
            "name": "Test",
            "assets": ["SPY"],
            "timeframe": "1d",
            "params": {"fast": 5},
            "code": code,
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert create.status_code == 200
    strategy_id = create.json()["id"]
    get = client.get(f"/strategies/{strategy_id}", headers={"Authorization": f"Bearer {token}"})
    assert get.status_code == 200
    update = client.put(
        f"/strategies/{strategy_id}",
        json={"name": "Updated"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert update.status_code == 200
    delete = client.delete(f"/strategies/{strategy_id}", headers={"Authorization": f"Bearer {token}"})
    assert delete.status_code == 204
