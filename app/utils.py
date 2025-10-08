from flask import jsonify

def json_response(data=None, message=None, status="success", code=200, **kwargs):
    response = {
        "data": data,
        "message": message,
        "status": status
    }

    response.update(kwargs)

    return jsonify(response), code