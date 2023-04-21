from flask import Blueprint, jsonify, current_app, request, abort
from models.concert import Concert
import uuid
import psutil, os
import datetime
import requests
concerts_blueprint = Blueprint("concerts", __name__)


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
    else:
        # If the service is not healthy, return a 500 status code
        return jsonify({"error": "Service is not healthy."}), 500



@concerts_blueprint.route("/concerts", methods=["GET"])
def get_all_concerts():
    # get all concerts
    concerts_data = current_app.db_concerts.find({}, projection={"_id": 0, "svg":0})
    concerts = [Concert(**concert_data).to_dict() for concert_data in concerts_data]
    return jsonify(concerts), 200


def valid_date(date):
    try:
        datetime.datetime.strptime(date, "%Y-%m-%d").date()
        return True
    except ValueError:
        return False

def valid_status(status):
    allowed_statuses = ("ACTIVE", "CANCELLED", "SOLD_OUT")
    if status not in allowed_statuses:
        return False
    return True

@concerts_blueprint.route("/concerts", methods=["POST"])
def create_concert():
    data = request.get_json()

    # Check if all required fields are provided
    if not all(key in data for key in ("name", "venue", "date", "capacity", "status")):
        abort(400, description="name, date, location, capacity and status are required in the request body")

    # Validate the capacity field
    try:
        capacity = int(data["capacity"])
    except ValueError:
        abort(400, description="Capacity should be a integer")

    # Validate the status field
    allowed_statuses = ("ACTIVE", "CANCELLED", "SOLD_OUT")
    if data["status"] not in allowed_statuses:
        abort(400, description=f"Status should be one of {', '.join(allowed_statuses)}")


    # Validate the date format
    try:
        concert_date = datetime.datetime.strptime(data["date"], "%Y-%m-%d").date()
    except ValueError:
        abort(400, description="Invalid date format. Date should be in YYYY-MM-DD format.")


    # Create a new ticket with a unique ID and ACTIVE status
    concert_id = str(uuid.uuid4())
    concert = {
        "id": concert_id,
        "name": data["name"],
        "venue": data["venue"],
        "date": data["date"],
        "capacity": data["capacity"],
        "status": data["status"],
    }

    try:
        # save to db
        current_app.db_concerts.insert_one(concert)
    except Exception as e:
        current_app.logger.error(f"{e}")
        abort(500, description=f"An unknown error occurred: {e}")

    concert_response = {
        "id": concert["id"],
        "name": concert["name"],
        "venue": concert["venue"],
        "date": concert["date"],
        "capacity": concert["capacity"],
        "status": concert["status"],
    }
    # request  to generate svg
    request_hamilton(concert_id)
    current_app.db_concerts.update_one({"id": concert_id}, {"$set": {"print_status": "PENDING"}})
    #todo: update to db
    
    return jsonify(concert_response), 200

def request_hamilton(concert_id):
    try:
        response = requests.post(
            f"{current_app.config['SERVICE_HAMILTON_URL']}/concerts/{concert_id}", json={})
    except Exception as e:
        current_app.logger.error(f"{e}")
        abort(500, description=f"An unknown error occurred: {e}")


@concerts_blueprint.route("/concerts/<concert_id>", methods=["GET"])
def get_concert_by_id(concert_id):
    if concert_id == "health":
        return health_check()
    concert_data = current_app.db_concerts.find_one({"id": concert_id}, projection={"_id": 0, "svg":0})
    if not concert_data:
        abort(404, description=f"Concert with id {concert_id} does not exist")
    return jsonify(concert_data), 200

@concerts_blueprint.route("/concerts/<string:concert_id>", methods=["PUT"])
def update_concert(concert_id):
    concert_data = current_app.db_concerts.find_one({"id": concert_id})
    
    if not concert_data:
        abort(404, description=f"Concert with id {concert_id} does not exist")

    update_data = request.get_json()

    if not update_data:
        abort(400, description="No valid data provided in the request body")

    allowed_updates = {"name", "venue", "date", "status"}

    for key in update_data.keys():
        if key not in allowed_updates:
            abort(400, description=f"Invalid field: {key}. Cannot update {key}.")

    # todo check valid of date
    if "date" in update_data:
        if not valid_date(update_data["date"]):
            abort(400, description="Invalid date format. Date should be in YYYY-MM-DD format.")
    # valid of status
    if "status" in update_data:
        if not valid_status(update_data["status"]):
            abort(400, description=f"Status should be one of {', '.join(allowed_statuses)}")

    # Update concert details in the database
    current_app.db_concerts.update_one({"id": concert_id}, {"$set": update_data})

    # remove svg file if it exist in db_concerts
    result = current_app.db_concerts.update_one(
        {"id": concert_id},
        {"$unset": {"svg": ""}}
    )

    updated_concert = current_app.db_concerts.find_one({"id": concert_id}, projection={"_id": 0, "svg":0})
    
    # request  to generate svg
    request_hamilton(concert_id)
    current_app.db_concerts.update_one({"id": concert_id}, {"$set": {"print_status": "PENDING"}})
    #todo: update to to pending
    

    return jsonify(updated_concert), 200


@tickets_blueprint.route("/concerts/<string:concert_id>/seats", methods=["GET"])
def get_printed_seat(concert_id):
    concert_data = current_app.db_concerts.find_one({"id": concert_id}, projection={"_id": 0})
    if not concert_data:
        return jsonify({"error": "The concert does not exist."}), 404

    return ticket_data["svg"], 200
