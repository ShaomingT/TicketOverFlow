import traceback

import boto3
from flask import Blueprint, jsonify, request, current_app, abort, Response, make_response
from models.ticket import Ticket
from models.user import User
from models.concert import Concert
from models import db
import uuid
import json

tickets_blueprint = Blueprint("tickets", __name__)


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


def valid_uuid(uuid_str):
    try:
        uuid.UUID(uuid_str)
        return True
    except ValueError:
        return False


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
        tickets = Ticket.query.all()
        response_list = []
        for ticket in tickets:
            response_list.append({
                "id": ticket.id,
                "concert": {
                    "id": ticket.concert_id,
                    "url": f"{current_app.config['SERVICE_CONCERT_URL']}/{ticket.concert_id}"
                },
                "user": {
                    "id": ticket.user_id,
                    "url": f"{current_app.config['SERVICE_USER_URL']}/{ticket.user_id}"
                },
                "print_status": ticket.print_status,
            })
        return jsonify(response_list), 200

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
                "url": f"{current_app.config['SERVICE_CONCERT_URL']}/{ticket.concert_id}"
            },
            "user": {
                "id": ticket.user_id,
                "url": f"{current_app.config['SERVICE_USER_URL']}/{ticket.user_id}"
            },
            "print_status": ticket.print_status,
        })
    return jsonify(response_list), 200


def request_hamilton_concert(concert_id):
    try:
        # create a boto3 client
        sqs = boto3.client('sqs')
        # your queue url
        queue_url = current_app.config['SQS_QUEUE_URL']
        # create the message body
        message_body = {
            "event": "concert",
            "id": str(concert_id)
        }
        # send the message
        response = sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps(message_body),
        )

        # log the message id
        current_app.logger.info(f"Message sent to Hamilton queue. Message ID: {response['MessageId']}")

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

    # if concert_id or user_id not valid, return 400
    if not valid_uuid(concert_id) or not valid_uuid(user_id):
        abort(400, description="concert_id or user_id is not valid")

    # Check if concert_id and user_id are provided
    if not all(key in data for key in ("concert_id", "user_id")):
        abort(400, description="concert_id and user_id are required in the request body")

    current_app.logger.debug(f"Check the existing of concert {concert_id}, and user {user_id}")
    concert = Concert.query.filter_by(id=data["concert_id"]).first()
    user = User.query.filter_by(id=data["user_id"]).first()

    if not concert or not user:
        current_app.logger.info("concert or user does not exist")
        abort(400, description="concert or user does not exist")

    num_tickets_sold = Ticket.query.filter_by(concert_id=data["concert_id"]).count()

    if num_tickets_sold >= concert.capacity:
        concert.status = "SOLD_OUT"
        db.session.commit()
        current_app.logger.info("concert is full")
        abort(422, description="concert is full")

    # Create a new ticket with a unique ID and NOT_PRINTED status
    ticket_id = str(uuid.uuid4())
    ticket = Ticket(
        id=ticket_id,
        concert_id=data["concert_id"],
        user_id=data["user_id"],
        print_status="NOT_PRINTED"
    )

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

    return jsonify(ticket_response), 201


@tickets_blueprint.route("/tickets/<string:ticket_id>", methods=["GET"])
def get_ticket_by_id(ticket_id):
    if ticket_id == "health":
        return health_check()
    if valid_uuid(ticket_id) is False:
        return jsonify({"error": "The ticket id is not valid."}), 404
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


def request_hamilton(ticket_id):
    try:
        # create a boto3 client
        sqs = boto3.client('sqs')
        # your queue url
        queue_url = current_app.config['SQS_QUEUE_URL']
        # create the message body
        message_body = {
            "event": "ticket",
            "id": str(ticket_id)
        }
        # send the message
        response = sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps(message_body),
        )

        # log the message id
        current_app.logger.info(f"Message sent to Hamilton queue. Message ID: {response['MessageId']}")

    except Exception as e:
        current_app.logger.error(f"{e}")
        abort(500, description=f"An unknown error occurred: {e}")


@tickets_blueprint.route("/tickets/<string:ticket_id>/print", methods=["POST"])
def print_ticket(ticket_id):
    if valid_uuid(ticket_id) is False:
        return jsonify({"error": "The ticket id is not valid."}), 404
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
    # verify ticket_id
    if valid_uuid(ticket_id) is False:
        return jsonify({"error": "The ticket id is not valid."}), 404
    # ticket_data = current_app.db_tickets.find_one({"id": ticket_id}, projection={"_id": 0})
    ticket = Ticket.query.filter_by(id=ticket_id).first()
    ticket_data = ticket.to_dict() if ticket else None
    if not ticket_data:
        return jsonify({"error": "The ticket does not exist or has not been printed yet."}), 404

    if ticket_data["print_status"] != "PRINTED":
        return jsonify({"error": "The ticket is being pending for printing."}), 404

    response = make_response(ticket_data["svg"])
    response.headers.set('Content-Type', 'image/svg+xml')
    return response
