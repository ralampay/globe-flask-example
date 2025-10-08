from flask import Blueprint, request
from app.models import User
from app.utils import json_response
from app import db

users_bp = Blueprint("users", __name__, url_prefix="/users")

@users_bp.route("", methods=["POST"])
def create():
    payload = request.get_json() or {}

    email = payload.get("email")
    first_name = payload.get("first_name")
    last_name = payload.get("last_name")

    errors = {}

    if not email:
        errors["email"] = "required"

    if not first_name:
        errors["first_name"] = "required"

    if not last_name:
        errors["last_name"] = "required"

    if len(errors) > 0:
        return json_response(
            data={ "errors": errors },
            status="error",
            message="Something went wrong",
            code=422
        )

    user = User(
        email=email,
        first_name=first_name,
        last_name=last_name
    )

    db.session.add(user)
    db.session.commit()

    return json_response(
        data=user.to_dict(),
        status="success",
        message="Created user"
    )

# /users
@users_bp.route("", methods=["GET"])
def index():
    users = [u.to_dict() for u in User.query.all()]

    return json_response(
        data=users,
        message="list of users",
        status="success"
    )

# /users/{id}:type uuid
@users_bp.route("/<uuid:id>", methods=["GET"])
def show(id):
    user = User.query.get(id)

    if not user:
        return json_response(
            data=None,
            message="not found",
            status="error",
            code=404
        )
    else:
        return json_response(
            data=user.to_dict(),
            message="returning user",
            status="success"
        )