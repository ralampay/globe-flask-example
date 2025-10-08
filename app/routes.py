from flask import Blueprint, jsonify

api = Blueprint("api", __name__)

@api.route("/heartbeat", methods=["POST"])
def heartbeat():
    return jsonify({
        "message": "success"
    }), 200