from flask import Blueprint, jsonify, current_app
from models.user import User
import logging

users_blueprint = Blueprint("users", __name__)


def health_check():
    """
    Note: 503 code will be automatically returned to client by Flask.
    :return:
    """
    try:
        response_data = {
            "healthy": True,
        }
        return jsonify(response_data), 200
    except Exception as e:
        # If there's an error, return a 503 status code indicating the service is not healthy
        current_app.logger.error(f"Health check failed: {e}")
        return jsonify({"error": "Service is not healthy."}), 503


@users_blueprint.route("/users", methods=["GET"])
def get_all_users():
    try:
        logging.info("Handling request for /api/v1/users")
        users_data = User.query.all()
        users_data = [user.to_dict() for user in users_data]
        return jsonify(users_data), 200
    except Exception as e:
        logging.error(f"Error in get_all_users: {e}")
        return jsonify({"error": "Internal server error./users"}), 500


@users_blueprint.route("/users/<string:user_id>", methods=["GET"])
def get_user_by_id(user_id):
    if user_id == "health":
        return health_check()
    try:
        user_data = User.query.get(user_id)
        if user_data is not None:
            user_data = user_data.to_dict()
            return jsonify(user_data), 200
        else:
            return jsonify({"error": "User not found."}), 404
    except Exception as e:
        current_app.logger.info(f"Error getting user by id: {e}")
        # return a json response with an error message and a 500 status code
        return jsonify({"error": "The user does not exist."}), 404
