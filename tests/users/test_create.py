def test_successfully_create_user(client, app):
    payload = {
        "email": "user@example.com",
        "first_name": "Raphael",
        "last_name": "Alampay"
    }

    response = client.post("/users", json=payload)

    data = response.get_json()

    from app.models import User

    with app.app_context():
        expected_count = 1
        created_user_email = data["data"]["email"]
        created_user = User.query.filter_by(
            email=created_user_email
        ).first()

        assert response.status_code == 200
        assert data["status"] == "success"
        assert data["data"]["email"] == payload["email"]
        assert expected_count == len(User.query.all())
        assert created_user is not None

def test_required_parameters(client):
    payload = {}
    # 1. It should return 422
    response = client.post("/users", json=payload)

    assert response.status_code == 422

    # 2. It should assert a data block that contains error messages:
    data = response.get_json()
    assert isinstance(data["data"]["errors"], dict)
    assert data["data"]["errors"]["email"] == "required"
    assert data["data"]["errors"]["last_name"] == "required"
    assert data["data"]["errors"]["first_name"] == "required"
