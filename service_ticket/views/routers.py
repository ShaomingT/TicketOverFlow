import requests
from flask import Blueprint, jsonify, request, current_app
from models.ticket import Ticket

tickets_blueprint = Blueprint("tickets", __name__)

USER_SERVICE_URL = "http://localhost:8888/api/v1/users"
CONCERT_SERVICE_URL = "http://localhost:7777/api/v1/concerts"


@tickets_blueprint.route("/tickets/test", methods=["GET"])
def test():
    return "Tickets service is up and running!", 200


@tickets_blueprint.route("/tickets/health", methods=["GET"])
def health_check():
    try:
        # Add any other health checks for your service here
        return "", 200
    except Exception as e:
        return str(e), 500

@tickets_blueprint.route("/tickets", methods=["GET"])
def get_all_tickets():
    tickets_data = list(current_app.db.find({}, projection={"_id": 0}))
    tickets = [Ticket(**ticket_data) for ticket_data in tickets_data]
    for ticket in tickets:
        user = get_user(ticket.user_id)
        if user:
            ticket.user = user
    return jsonify([ticket.to_dict() for ticket in tickets]), 200

@tickets_blueprint.route("/tickets", methods=["POST"])
def create_ticket():
    request_data = request.get_json()
    user_id = request_data.get("user_id")
    concert_id = request_data.get("concert_id")

    user = get_user(user_id)
    concert = get_concert(concert_id)

    if user and concert:
        ticket = Ticket.create_new_ticket(user_id, concert_id, current_app.db)
        ticket.user = user
        ticket.concert = concert
        return jsonify(ticket.to_dict()), 200
    else:
        return jsonify({"error": "Invalid user or concert ID."}), 400

@tickets_blueprint.route("/tickets/<string:ticket_id>", methods=["GET"])
def get_ticket_by_id(ticket_id):
    ticket_data = current_app.db.find_one({"id": ticket_id}, projection={"_id": 0})
    if ticket_data:
        ticket = Ticket(**ticket_data)
        user = get_user(ticket.user_id)
        if user:
            ticket.user = user
        return jsonify(ticket.to_dict()), 200
    else:
        return jsonify({"error": "The ticket does not exist."}), 404



@tickets_blueprint.route("/tickets/<string:ticket_id>/print", methods=["POST"])
def print_ticket(ticket_id):
    return jsonify({"error": "developing"}), 404

@tickets_blueprint.route("/tickets/<string:ticket_id>/print", methods=["GET"])
def get_printed_ticket(ticket_id):
    return jsonify({"error": "developing"}), 404

