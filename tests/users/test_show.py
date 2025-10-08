from app.utils import build_headers

def test_show(client, mock_user):
    response = client.get(f"/users/{mock_user.id}", headers=build_headers())

    assert response.status_code == 200

    data = response.get_json()
    assert data["data"]["id"] == str(mock_user.id)
    assert data["data"]["email"] == mock_user.email
    assert data["data"]["first_name"] == mock_user.first_name
    assert data["data"]["last_name"] == mock_user.last_name

# Exercise 1:
# 1. Create a test method test_not_found
# 2. Assert that the status code is 404
# 3. Pass the test in def show of users_controller
def test_not_found(client, mock_user):
    import uuid
    id = str(uuid.uuid4())
    response = client.get(f"/users/{id}", headers=build_headers())

    assert response.status_code == 404
