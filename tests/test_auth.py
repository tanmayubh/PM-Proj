def test_login_invalid_credentials(client):
    response = client.post(
        "/auth/login",
        data={"username": "nope", "password": "wrong"}
    )
    assert response.status_code == 401