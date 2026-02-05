def test_create_project_unauthorized(client):
    response = client.post("/projects", json={"name": "Test"})
    assert response.status_code in (401, 403)