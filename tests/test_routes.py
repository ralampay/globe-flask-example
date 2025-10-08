def test_404_route(client):
    response = client.get("/doesnotexist")
    json_data = response.get_json()

    assert response.status_code == 404
    assert json_data["status"] == "error"
    assert json_data["message"] == "not found"

def test_heartbeat(client):
    response = client.post("/heartbeat")
    json_data = response.get_json()

    assert response.status_code == 200
    assert json_data["message"] == "success"