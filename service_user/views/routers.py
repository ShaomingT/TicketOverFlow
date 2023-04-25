from flask import Blueprint, jsonify, current_app, abort
from models.user import User
import os
import psutil
import logging

users_blueprint = Blueprint("users", __name__)


def health_check():
    try:
        # Check dependencies or other conditions for a healthy service
        # If everything is OK, return a 200 status code with health information
        # process = psutil.Process(os.getpid())
        # memory_usage = process.memory_info().rss / (1024 * 1024)  # Convert to MB
        # cpu_usage = process.cpu_percent()

        response_data = {
            "healthy": True,
            # "dependencies": [
            #     {
            #         "name": "database",
            #         "healthy": True
            #     }
            # ],
            # "memoryUsage": f"{memory_usage:.2f}MB",
            # "cpuUsage": f"{cpu_usage:.2f}%"
        }

        # If the CPU usage is above 98%, return a 500 status code
        # if cpu_usage > 98:
        #     current_app.logger.error(f"Health check failed: CPU usage is too high")
        #     return jsonify({"error": "Service is not running optimally."}), 503

        return jsonify(response_data), 200
    except Exception as e:
        # If there's an error, return a 503 status code indicating the service is not healthy
        current_app.logger.error(f"Health check failed: {e}")
        return jsonify({"error": "Service is not healthy."}), 500


@users_blueprint.route("/users", methods=["GET"])
def get_all_users():
    try:
        logging.info("Handling request for /api/v1/users")  # Add this line
        users_data = User.query.all()
        users_data = [user.to_dict() for user in users_data]
        return jsonify(users_data), 200
    except Exception as e:
        logging.error(f"Error in get_all_users: {e}")  # Add this line
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
