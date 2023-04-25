from flask import Blueprint, jsonify, current_app, request, abort
from models.concert import Concert
from models.user import User
from models.ticket import Ticket
from models import db
import uuid
import psutil
import os
import datetime
import requests

concerts_blueprint = Blueprint("concerts", __name__)


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


@concerts_blueprint.route("/concerts", methods=["GET"])
def get_all_concerts():
    # get all concerts
    # concerts_data = current_app.db_concerts.find({}, projection={"_id": 0, "id": 1, "name": 1, "venue": 1, "date": 1,
    #                                                              "capacity": 1, "status": 1})
    # concerts = [Concert(**concert_data).to_dict() for concert_data in concerts_data]
    # return jsonify(concerts), 200
    #
    # sqlalchemy sql query to get all concerts, with the field id, name, venue, date, capacity and status
    concerts = Concert.query.all()
    concerts_list = [concert.to_dict() for concert in concerts]
    allowed_fields = {"id", "name", "venue", "date", "capacity", "status"}
    # only allowed_fields can be returned
    filtered_concerts_list = [
        {key: concert[key] for key in concert.keys() if key in allowed_fields}
        for concert in concerts_list
    ]
    return jsonify(filtered_concerts_list), 200


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

    # if there is invalid field, return 400
    allowed_fields = {"name", "venue", "date", "capacity", "status"}
    for key in data.keys():
        if key not in allowed_fields:
            abort(400, description=f"Invalid field: {key}. Cannot update {key}.")

    # Validate the capacity field
    try:
        capacity = int(data["capacity"])
    except ValueError:
        abort(400, description="Capacity should be a integer")

    if capacity <= 0:
        abort(400, description="Capacity should be greater than 0")

    # Validate the status field
    allowed_statuses = ("ACTIVE", "CANCELLED", "SOLD_OUT")
    if data["status"] not in allowed_statuses:
        abort(400, description=f"Status should be one of {', '.join(allowed_statuses)}")

    # Validate the date format
    try:
        datetime.datetime.strptime(data["date"], "%Y-%m-%d").date()
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
        # current_app.db_concerts.insert_one(concert)
        new_concert = Concert(**concert)
        db.session.add(new_concert)
        db.session.commit()
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
    # current_app.db_concerts.update_one({"id": concert_id}, {"$set": {"print_status": "PENDING"}})
    concert = Concert.query.filter_by(id=concert_id).first()
    db.session.close()
    if concert:
        concert.print_status = "PENDING"
        db.session.commit()
    # todo: update to db

    return jsonify(concert_response), 200


def request_hamilton(concert_id):
    try:
        response = requests.post(
            f"{current_app.config['SERVICE_HAMILTON_URL']}", json={"event": "concert",
                                                                   "id": concert_id})
        if response.status_code != 202:
            current_app.logger.error(f"Error requesting Hamilton service: {response.json()}")
            abort(500, description=f"Error requesting Hamilton service: {response.json()}")
    except Exception as e:
        current_app.logger.error(f"{e}")
        abort(500, description=f"An unknown error occurred: {e}")


@concerts_blueprint.route("/concerts/<concert_id>", methods=["GET"])
def get_concert_by_id(concert_id):
    if concert_id == "health":
        return health_check()
    # Check if the concert_id is a valid UUID
    try:
        uuid.UUID(concert_id, version=4)
    except ValueError:
        abort(404, description=f"Invalid concert id: {concert_id}")

    # concert_data = current_app.db_concerts.find_one({"id": concert_id},
    #                                                 projection={"_id": 0, "svg": 0, "print_status": 0})
    concert = Concert.query.filter_by(id=concert_id).first()
    db.session.close()

    if concert:
        concert_data = concert.to_dict(exclude_fields=["svg", "print_status", "svg_seat_num"])
    else:
        concert_data = None
    if not concert_data:
        abort(404, description=f"Concert with id {concert_id} does not exist")
    return jsonify(concert_data), 200


@concerts_blueprint.route("/concerts/<string:concert_id>", methods=["PUT"])
def update_concert(concert_id):
    try:
        uuid.UUID(concert_id, version=4)
    except ValueError:
        abort(404, description=f"Invalid concert id: {concert_id}")

    # concert_data = current_app.db_concerts.find_one({"id": concert_id})
    concert = Concert.query.filter_by(id=concert_id).first()
    db.session.close()
    concert_data = concert.to_dict() if concert else None

    if not concert_data:
        abort(404, description=f"Concert with id {concert_id} does not exist")

    update_data = request.get_json()

    if not update_data:
        abort(400, description="No valid data provided in the request body")

    allowed_updates = {"name", "venue", "date", "status", "capacity"}

    for key in update_data.keys():
        if key not in allowed_updates:
            abort(400, description=f"Invalid field: {key}. Cannot update {key}.")

    # todo check valid of date
    if "date" in update_data:
        if not valid_date(update_data["date"]):
            abort(400, description="Invalid date format. Date should be in YYYY-MM-DD format.")
    # valid of status
    allowed_statuses = ("ACTIVE", "CANCELLED", "SOLD_OUT")
    if "status" in update_data:
        if not valid_status(update_data["status"]):
            abort(400, description=f"Status should be one of {', '.join(allowed_statuses)}")

    # if capacity in update_data, it should >=0 and be int
    if "capacity" in update_data:
        try:
            capacity = int(update_data["capacity"])
            if capacity <= 0:
                return jsonify({"error": "Capacity should be greater than 0"}), 400
        except ValueError:
            return jsonify({"error": "Capacity should be a integer"}), 400

    # Update concert details in the database
    # current_app.db_concerts.update_one({"id": concert_id}, {"$set": update_data})

    concert = Concert.query.filter_by(id=concert_id).first()
    db.session.close()
    for key, value in update_data.items():
        setattr(concert, key, value)
    db.session.commit()

    # remove svg file if it exists in db_concerts
    # current_app.db_concerts.update_one(
    #     {"id": concert_id},
    #     {"$unset": {"svg": ""}}
    # )
    if concert:
        concert.svg = None
        concert.svg_seat_num = None
        db.session.commit()

    # updated_concert = current_app.db_concerts.find_one({"id": concert_id},
    #                                                    projection={"_id": 0, "svg": 0, "print_status": 0})
    #
    concert = Concert.query.filter_by(id=concert_id).first()
    db.session.close()
    if concert:
        updated_concert = {attr: getattr(concert, attr) for attr in
                           ['id', 'name', 'venue', 'date', 'capacity', 'status']}
    else:
        updated_concert = None

    # request  to generate svg
    request_hamilton(concert_id)
    #    current_app.db_concerts.update_one({"id": concert_id}, {"$set": {"print_status": "PENDING"}})
    concert = Concert.query.filter_by(id=concert_id).first()
    db.session.close()
    if concert:
        concert.print_status = "PENDING"
        db.session.commit()

    return jsonify(updated_concert), 200


@concerts_blueprint.route("/concerts/<string:concert_id>/seats", methods=["GET"])
def get_printed_seat(concert_id):
    concert_data = Concert.query.filter_by(id=concert_id).first()
    db.session.close()
    if concert_data:
        concert_data = concert_data.to_dict()

    # if concert does not exist, return 404
    if not concert_data:
        return jsonify({"error": "The concert does not exist."}), 404

    # if svg field not exit or is None, return 404
    if "svg" not in concert_data or concert_data["svg"] is None:
        return jsonify({"error": "The concert does not have a svg file."}), 404

    return concert_data["svg"], 200
