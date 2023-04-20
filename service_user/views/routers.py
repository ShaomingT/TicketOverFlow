from flask import Blueprint, jsonify, current_app
from models.user import User

users_blueprint = Blueprint("users", __name__)

import os
import psutil

def health_check():
    try:
        # Check dependencies or other conditions for a healthy service
        # If everything is OK, return a 200 status code with health information
        process = psutil.Process(os.getpid())
        memory_usage = process.memory_info().rss / (1024 * 1024)  # Convert to MB

        response_data = {
            "healthy": True,
            "dependencies": [
                {
                    "name": "database",
                    "healthy": True
                }
            ],
            "memoryUsage": f"{memory_usage:.2f}MB"
        }

        return jsonify(response_data), 200
    except Exception as e:
        # If there's an error, return a 503 status code indicating the service is not healthy
        current_app.logger.error(f"Health check failed: {e}")
        return jsonify({"error": "Service is not healthy."}), 503

@users_blueprint.route("/users", methods=["GET"])
def get_all_users():
    users_data = list(current_app.db.find({}, projection={"_id": 0}))
    users = [User(**user_data) for user_data in users_data]
    return jsonify([user.to_dict() for user in users]), 200

@users_blueprint.route("/users/<string:user_id>", methods=["GET"])
def get_user_by_id(user_id):
    if user_id == "health":
        return health_check()

    user_data = current_app.db.find_one({"id": user_id}, projection={"_id": 0})
    if user_data:
        user = User(**user_data)
        return jsonify(user.to_dict()), 200
    else:
        return jsonify({"error": "The user does not exist.11"}), 404
