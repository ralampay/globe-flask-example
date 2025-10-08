from app.utils import build_headers

def test_user_not_logged_in(client):
    response = client.get("/users")

    assert response.status_code == 401

def test_index(client, mock_user):
    response = client.get("/users", headers=build_headers())

    assert response.status_code == 200

    data = response.get_json()

    assert data["status"] == "success"
    assert data["message"] == "list of users"

    # Assert 1: Check if data is a list
    assert isinstance(data["data"], list)

    # Assert 2: Check length of list == 1
    assert len(data["data"]) == 1

    # Assert 3: Check if user id of data[0]['id'] == mock_user.id
    assert data["data"][0]['id'] == str(mock_user.id)
    assert data["data"][0]['email'] == mock_user.email