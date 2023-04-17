from flask import Blueprint, jsonify, current_app
from models.user import User

users_blueprint = Blueprint("users", __name__)

@users_blueprint.route("/users", methods=["GET"])
def get_all_users():
    users_data = list(current_app.db.find({}, projection={"_id": 0}))
    users = [User(**user_data) for user_data in users_data]
    return jsonify([user.to_dict() for user in users]), 200

@users_blueprint.route("/users/<string:user_id>", methods=["GET"])
def get_user_by_id(user_id):
    user_data = current_app.db.find_one({"id": user_id}, projection={"_id": 0})
    if user_data:
        user = User(**user_data)
        return jsonify(user.to_dict()), 200
    else:
        return jsonify({"error": "The user does not exist."}), 404
