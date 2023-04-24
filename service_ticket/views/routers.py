import traceback

import requests
from flask import Blueprint, jsonify, request, current_app, abort
from models.ticket import Ticket
from models.user import User
from models.concert import Concert
from models import db
import uuid
import psutil
import os

tickets_blueprint = Blueprint("tickets", __name__)


def health_check():
    try:
        # Check dependencies or other conditions for a healthy service
        # If everything is OK, return a 200 status code with health information
        process = psutil.Process(os.getpid())
        memory_usage = process.memory_info().rss / (1024 * 1024)  # Convert to MB
        cpu_usage = process.cpu_percent()

        response_data = {
            "healthy": True,
            "dependencies": [
                {
                    "name": "database",
                    "healthy": True
                }
            ],
            "memoryUsage": f"{memory_usage:.2f}MB",
            "cpuUsage": f"{cpu_usage:.2f}%"
        }

        # If the CPU usage is above 98%, return a 500 status code
        if cpu_usage > 98:
            current_app.logger.error(f"Health check failed: CPU usage is too high")
            return jsonify({"error": "Service is not running optimally."}), 503

        return jsonify(response_data), 200
    except Exception as e:
        # If there's an error, return a 503 status code indicating the service is not healthy
        current_app.logger.error(f"Health check failed: {e}")
        return jsonify({"error": "Service is not healthy."}), 500


@tickets_blueprint.route("/tickets", methods=["GET"])
def get_all_tickets():
    # Check for unknown filter parameters
    allowed_params = {"user_id", "concert_id"}
    for param in request.args:
        if param not in allowed_params:
            return jsonify({"error": f"Unknown identifier provided as filter parameter"}), 404

    # Get the query parameters
    user_id = request.args.get("user_id")
    concert_id = request.args.get("concert_id")

    # check if the user_id and concert_id are valid uuid, if not return 404
    if user_id:
        try:
            uuid.UUID(user_id)
        except ValueError:
            return jsonify({"error": "Unknown identifier provided as filter parameter"}), 404
    if concert_id:
        try:
            uuid.UUID(concert_id)
        except ValueError:
            return jsonify({"error": "Unknown identifier provided as filter parameter"}), 404

    # if no parameters are provided, return all tickets
    if not user_id and not concert_id:
        # tickets_data = list(current_app.db_tickets.find({}, projection={"_id": 0, "svg": 0}))
        # tickets = [Ticket(**ticket_data) for ticket_data in tickets_data]
        # return jsonify([ticket.to_dict() for ticket in tickets]), 200
        tickets = Ticket.query.all()
        return jsonify(
            [ticket.to_dict(include_fields=['id', 'concert', 'user', 'print_status']) for ticket in tickets]), 200

    # Build the query based on the parameters
    query = {}
    if user_id:
        query["user_id"] = user_id
    if concert_id:
        query["concert_id"] = concert_id

    # List all the purchased tickets based on the query
    # tickets_data = list(current_app.db_tickets.find(query, projection={"_id": 0, "svg": 0}))
    tickets = Ticket.query.filter_by(**query).all()
    if len(tickets) == 0:
        return jsonify({"error": "Unknown identifier provided as filter parameter"}), 404

    response_list = []
    for ticket in tickets:
        response_list.append({
            "id": ticket.id,
            "concert": {
                "id": ticket.concert_id,
                "url": f"{current_app.config['SERVICE_CONCERT_URL']}/concerts/{ticket.concert_id}"
            },
            "user": {
                "id": ticket.user_id,
                "url": f"{current_app.config['SERVICE_USER_URL']}/users/{ticket.user_id}"
            },
            "print_status": ticket.print_status,
        })
    return jsonify(response_list), 200


def request_hamilton_concert(concert_id):
    try:
        response = requests.post(
            f"{current_app.config['SERVICE_HAMILTON_URL']}", json={"event": "concert",
                                                                   "id": str(concert_id)})
    except Exception as e:
        current_app.logger.error(f"{e}")
        abort(500, description=f"An unknown error occurred: {e}")


@tickets_blueprint.route("/tickets", methods=["POST"])
def create_ticket():
    # Parse the request data
    data = request.get_json()
    # define concert_id
    concert_id = data["concert_id"]
    user_id = data["user_id"]

    # Check if concert_id and user_id are provided
    if not all(key in data for key in ("concert_id", "user_id")):
        abort(400, description="concert_id and user_id are required in the request body")

    current_app.logger.debug(f"Check the existing of concert {concert_id}, and user {user_id}")
    # Check if concert and user exist
    # concert = current_app.db_concerts.find_one({"id": data["concert_id"]})
    # user = current_app.db_users.find_one({"id": data["user_id"]})
    concert = Concert.query.filter_by(id=data["concert_id"]).first()
    user = User.query.filter_by(id=data["user_id"]).first()

    if not concert or not user:
        current_app.logger.info("concert or user does not exist")
        abort(400, description="concert or user does not exist")

    # Check if the concert is full
    # num_tickets_sold = current_app.db_tickets.count_documents({"concert.id": data["concert_id"]})
    #
    # # if the number of tickets sold is equal to the maximum capacity of the concert, mark the concert status as SOLD_OUT
    # if num_tickets_sold >= concert["capacity"]:
    #     current_app.db_concerts.update_one({"id": concert["id"]}, {"$set": {"status": "SOLD_OUT"}})
    #     current_app.logger.info("concert is full")
    #     abort(400, description="concert is full")
    num_tickets_sold = Ticket.query.filter_by(concert_id=data["concert_id"]).count()

    if num_tickets_sold >= concert.capacity:
        concert.status = "SOLD_OUT"
        db.session.commit()
        current_app.logger.info("concert is full")
        abort(400, description="concert is full")

    # Create a new ticket with a unique ID and NOT_PRINTED status
    ticket_id = str(uuid.uuid4())
    # ticket = {
    #     "id": ticket_id,
    #     "concert": {"id": data["concert_id"]},
    #     "user": {"id": data["user_id"]},
    #     "print_status": "NOT_PRINTED"
    # }
    ticket = Ticket(
        id=ticket_id,
        concert_id=data["concert_id"],
        user_id=data["user_id"],
        print_status="NOT_PRINTED"
    )

    # Insert the ticket into the database
    # try:
    #     current_app.db_tickets.insert_one(ticket)
    #     # update the concert svg in the database
    #     request_hamilton_concert(concert["id"])
    #     # update the ocncert's print_status to "PENDING"
    #     current_app.db_concerts.update_one({"id": concert_id}, {"$set": {"print_status": "PENDING"}})
    # except Exception as e:
    #     current_app.logger.error(f"{e}")
    #     abort(500, description=f"An unknown error occurred: {e}")
    try:
        db.session.add(ticket)
        db.session.commit()
        request_hamilton_concert(concert.id)
        concert.print_status = "PENDING"
        db.session.commit()
    except Exception as e:
        # logging traceback
        current_app.logger.error(traceback.format_exc())
        abort(500, description=f"An unknown error occurred: {e}")

    # Prepare the response
    ticket_response = {
        "id": ticket_id,
        "concert": {
            "id": concert.id,
            "url": f"{current_app.config['SERVICE_CONCERT_URL']}/{concert.id}"
        },
        "user": {
            "id": user.id,
            "url": f"{current_app.config['SERVICE_USER_URL']}/{user.id}"
        },
        "print_status": "NOT_PRINTED"
    }

    return jsonify(ticket_response), 200


@tickets_blueprint.route("/tickets/<string:ticket_id>", methods=["GET"])
def get_ticket_by_id(ticket_id):
    if ticket_id == "health":
        return health_check()
    ticket_data = Ticket.query.filter_by(id=ticket_id).first()
    if ticket_data:
        # ticket_data = ticket_data.to_dict(include_fields=['id', 'concert_id', 'user_id', 'print_status'])
        # build response json file
        ticket_response = {
            "id": ticket_data.id,
            "concert": {
                "id": ticket_data.concert_id,
                "url": f"{current_app.config['SERVICE_CONCERT_URL']}/{ticket_data.concert_id}"
            },
            "user": {
                "id": ticket_data.user_id,
                "url": f"{current_app.config['SERVICE_USER_URL']}/{ticket_data.user_id}"
            },
            "print_status": ticket_data.print_status
        }
        return jsonify(ticket_response), 200
    else:
        return jsonify({"error": "The ticket does not exist."}), 404


#################################################################

def request_hamilton(ticket_id):
    try:
        response = requests.post(
            f"{current_app.config['SERVICE_HAMILTON_URL']}", json={
                "event": "ticket",
                "id": str(ticket_id)
            })
    except Exception as e:
        current_app.logger.error(f"{e}")
        abort(500, description=f"An unknown error occurred: {e}")


@tickets_blueprint.route("/tickets/<string:ticket_id>/print", methods=["POST"])
def print_ticket(ticket_id):
    # try:
    # ticket_data = current_app.db_tickets.find_one({"id": ticket_id}, projection={"_id": 0})
    ticket_data = Ticket.query.filter_by(id=ticket_id).first()
    if not ticket_data:
        return jsonify({"error": "The ticket does not exist."}), 404

    if ticket_data.print_status == "PENDING":
        return jsonify({"error": "still processing"}), 500
    elif ticket_data.print_status == "PRINTED":
        return jsonify({"error": "already printed"}), 500

    request_hamilton(ticket_id)
    # current_app.db_tickets.update_one({"id": ticket_id}, {"$set": {"print_status": "PENDING"}})
    ticket = Ticket.query.filter_by(id=ticket_id).first()
    ticket.print_status = "PENDING"
    db.session.commit()

    return jsonify({"status": "The asynchronous request was successfully started."}), 202


@tickets_blueprint.route("/tickets/<string:ticket_id>/print", methods=["GET"])
def get_printed_ticket(ticket_id):
    # ticket_data = current_app.db_tickets.find_one({"id": ticket_id}, projection={"_id": 0})
    ticket = Ticket.query.filter_by(id=ticket_id).first()
    ticket_data = ticket.to_dict() if ticket else None
    if not ticket_data:
        return jsonify({"error": "The ticket does not exist or has not been printed yet."}), 404

    if ticket_data["print_status"] != "PRINTED":
        return jsonify({"error": "The ticket is being pending for printing."}), 404

    return ticket_data["svg"], 200
