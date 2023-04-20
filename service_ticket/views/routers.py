import requests
from flask import Blueprint, jsonify, request, current_app, abort
from models.ticket import Ticket
import uuid
import psutil
import os, threading
import subprocess
from concurrent.futures import ThreadPoolExecutor

tickets_blueprint = Blueprint("tickets", __name__)

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

@tickets_blueprint.route("/tickets/test", methods=["GET"])
def test():
    return "Tickets service is up and running!", 200


@tickets_blueprint.route("/tickets", methods=["GET"])
def get_all_tickets():
    # Get the query parameters
    user_id = request.args.get("user_id")
    concert_id = request.args.get("concert_id")

    # Check for unknown filter parameters
    allowed_params = {"user_id", "concert_id"}
    for param in request.args:
        if param not in allowed_params:
            return jsonify({"error": f"Unknown identifier provided as filter parameter"}), 404

    # Build the query based on the parameters
    query = {}
    if user_id:
        query["user.id"] = user_id
    if concert_id:
        query["concert.id"] = concert_id

    # List all the purchased tickets based on the query
    tickets_data = list(current_app.db_tickets.find(query, projection={"_id": 0}))
    if len(tickets_data) == 0:
        return jsonify({"error": "Unknown identifier provided as filter parameter"}), 404
    tickets = [Ticket(**ticket_data) for ticket_data in tickets_data]

    return jsonify([ticket.to_dict() for ticket in tickets]), 200


@tickets_blueprint.route("/tickets", methods=["POST"])
def create_ticket():
    # Parse the request data
    data = request.get_json()

    # Check if concert_id and user_id are provided
    if not all(key in data for key in ("concert_id", "user_id")):
        abort(400, description="concert_id and user_id are required in the request body")

    # Check if concert and user exist
    concert = current_app.db_concerts.find_one({"id": data["concert_id"]})
    user = current_app.db_users.find_one({"id": data["user_id"]})

    if not concert or not user:
        current_app.logger.info("concert or user does not exist")
        abort(400, description="concert or user does not exist")

    # Check if the concert is full
    num_tickets_sold = current_app.db_tickets.count_documents({"concert.id": data["concert_id"]})
    if num_tickets_sold >= concert["capacity"]:
        current_app.logger.info("concert is full")
        abort(400, description="concert is full")


    # Create a new ticket with a unique ID and NOT_PRINTED status
    ticket_id = str(uuid.uuid4())
    ticket = {
        "id": ticket_id,
        "concert": { "id": data["concert_id"]},
        "user": {"id": data["user_id"]},
        "print_status": "NOT_PRINTED"
    }

    # Insert the ticket into the database
    try:
        current_app.db_tickets.insert_one(ticket)
    except Exception as e:
        abort(500, description=f"An unknown error occurred: {e}")

    # Prepare the response
    ticket_response = {
        "id": ticket_id,
        "concert": {
            "id": concert["id"],
            "url": f"{current_app.config['SERVICE_CONCERT_URL']}/{concert['_id']}"
        },
        "user": {
            "id": user["id"],
            "url": f"{current_app.config['SERVICE_USER_URL']}/{user['_id']}"
        },
        "print_status": "NOT_PRINTED"
    }

    return jsonify(ticket_response), 200


