def test_create_user(client):
    payload = {
        "username": "admin",
        "email": "admin@test.com",
        "password": "secret",
        "role": "admin"
    }

    response = client.post("/users", json=payload)
    assert response.status_code == 200
    assert response.json()["username"] == "admin"