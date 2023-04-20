from flask import Blueprint, jsonify, current_app, request
from models.concert import Concert

concerts_blueprint = Blueprint("concerts", __name__)

@concerts_blueprint.route("/concerts", methods=["GET"])
def get_all_concerts():
    concerts_data = list(current_app.db.find({}, projection={"_id": 0}))
    concerts = [Concert(**concert_data) for concert_data in concerts_data]
    return jsonify([concert.to_dict() for concert in concerts]), 200

@concerts_blueprint.route("/concerts/<string:concert_id>", methods=["GET"])
def get_concert_by_id(concert_id):
    concert_data = current_app.db.find_one({"id": concert_id}, projection={"_id": 0})
    if concert_data:
        concert = Concert(**concert_data)
        return jsonify(concert.to_dict()), 200
    else:
        return jsonify({"error": "The concert does not exist."}), 404

@concerts_blueprint.route("/concerts", methods=["POST"])
def create_concert():
    concert_data = request.get_json()
    concert = Concert(**concert_data)
    current_app.db.insert_one(concert.to_dict())
    return jsonify(concert.to_dict()), 200

@concerts_blueprint.route("/concerts/<string:concert_id>", methods=["PUT"])
def update_concert(concert_id):
    concert_data = request.get_json()
    concert = current_app.db.find_one({"id": concert_id}, projection={"_id": 0})
    if concert:
        updated_concert = {**concert, **concert_data}
        current_app.db.update_one({"id": concert_id}, {"$set": updated_concert})
        # Call the other microservice to remove the existing tickets
        requests.delete(f'http://tickets.api.ticketoverflow.com/api/v1/tickets/{concert_id}')
        return jsonify(Concert(**updated_concert).to_dict()), 200
    else:
        return jsonify({"error": "The concert does not exist."}), 404

@concerts_blueprint.route("/concerts/<string:concert_id>/seats", methods=["GET"])
def get_seating_plan(concert_id):
    # Replace the placeholders with the actual command line tool's command and path
    command = "path/to/command_line_tool --input {concert_id}"
    svg_data = subprocess.check_output(command.format(concert_id=concert_id), shell=True)
    return svg_data, 200, {"Content-Type": "image/svg+xml"}
