from flask import jsonify, request

def json_response(data=None, message=None, status="success", code=200, **kwargs):
    response = {
        "data": data,
        "message": message,
        "status": status
    }

    response.update(kwargs)

    return jsonify(response), code

def build_headers():
    return {
        "Authorization": "Bearer example_token"
    }

def authenticate_user():
    # Only return if we have an error
    # Headers --> Authorization --> Bearer token
    token = request.headers.get("Authorization")

    if not token:
        return json_response(
            message="Unauthenticated",
            status="error",
            code=401
        )