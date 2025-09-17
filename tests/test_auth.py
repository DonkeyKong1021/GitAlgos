from app.db import models


def test_register_and_login(client):
    response = client.post(
        "/auth/register",
        json={"email": "user@example.com", "password": "Password123", "role": "admin"},
    )
    assert response.status_code == 201
    login = client.post(
        "/auth/login",
        json={"email": "user@example.com", "password": "Password123"},
    )
    assert login.status_code == 200
    tokens = login.json()
    assert "access_token" in tokens
    me = client.get("/auth/me", headers={"Authorization": f"Bearer {tokens['access_token']}"})
    assert me.status_code == 200
    assert me.json()["email"] == "user@example.com"
