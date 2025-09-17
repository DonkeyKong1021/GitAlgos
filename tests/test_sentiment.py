
def test_sentiment_endpoint(client):
    client.post(
        "/auth/register",
        json={"email": "sent@example.com", "password": "Password123", "role": "admin"},
    )
    login = client.post(
        "/auth/login",
        json={"email": "sent@example.com", "password": "Password123"},
    )
    token = login.json()["access_token"]
    response = client.get("/sentiment", params={"symbol": "AAPL"}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    body = response.json()
    assert "score" in body
    assert "rolling_score" in body
