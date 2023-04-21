from flask import Blueprint, jsonify, request, current_app, abort, current_app
from models.hamilton_ticket import HamiltonTicket
import uuid
import psutil
import os, threading, json
import subprocess
from threading import Thread
import logging
import traceback



hamilton_blueprint = Blueprint("hamilton", __name__)

@hamilton_blueprint.route("/hamilton/test", methods=["GET"])
def test():
    return "Hamilton service is up and running!", 200

###### generate ticket ######

def generate_ticket(ticket_input, app):
    try:
        with app.app_context():
            hamilton_path = app.config["HAMILTON_PATH"]
            ticket_id = ticket_input["id"]
            unique_id = uuid.uuid4()
            input_file = f"./temp/{ticket_id}_{unique_id}_input.json"
            print("input_file: ", input_file)
            with open(input_file, "w") as f:
                json.dump(ticket_input, f)
            output_file = f"./temp/{ticket_id}_{unique_id}_output"
            print("output_file: ", output_file)
            cmd = f"{hamilton_path} generate ticket --input {input_file} --output {output_file}"
            try:
                subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
                with open(f"{output_file}.svg", "r") as f:
                    svg_content = f.read()
                app.db_tickets.update_one({"id": ticket_id}, {"$set": {"print_status": "PRINTED", "svg": svg_content}})
                os.remove(input_file)
                os.remove(output_file + ".svg")
            except subprocess.CalledProcessError as e:
                logging.error(e.output)
                app.db_tickets.update_one({"id": ticket_id}, {"$set": {"print_status": "ERROR"}})
    except Exception as e:
        logging.error(e)
        logging.error(traceback.format_exc())
        app.db_tickets.update_one({"id": ticket_id}, {"$set": {"print_status": "ERROR: " + str(e)}})



@hamilton_blueprint.route("/hamilton/tickets/<string:ticket_id>", methods=["POST"])
def print_ticket(ticket_id):
    # get tickets data
    ticket_data = current_app.db_tickets.find_one({"id": ticket_id}, projection={"_id": 0})
    concert_id = ticket_data['concert']['id']
    concert_data = current_app.db_concerts.find_one({"id": concert_id}, projection={"_id": 0})
    user_id = ticket_data['user']['id']
    user_data = current_app.db_users.find_one({"id": user_id}, projection={"_id": 0})

    # svg payload
    svg_payload = {
        "id": ticket_data["id"],
        "name": user_data["name"],
        "email": user_data["email"],
        "concert": {
            "id": concert_data["id"],
            "name": concert_data["name"],
            "date": concert_data["date"],
            "venue": concert_data["venue"],
        }
    }


    app = current_app._get_current_object()
    Thread(target=generate_ticket, args=(svg_payload, app)).start()

    return jsonify({"status": "The asynchronous request was successfully started."}), 202


##### generat seat #####

def generate_concert(concert_input, app):
    try:
        with app.app_context():

            hamilton_path = app.config["HAMILTON_PATH"]
            concert_id = concert_input["id"]
            logging.debug(msg=f"concert_id: {concert_id}")
            logging.debug(msg=f"concert_input: {concert_input}")
            unique_id = uuid.uuid4()
            input_file = f"./temp/{concert_id}_{unique_id}_input.json"
            with open(input_file, "w") as f:
                json.dump(concert_input, f)
            output_file = f"./temp/{concert_id}_{unique_id}_output"
            cmd = f"{hamilton_path} generate seating --input {input_file} --output {output_file}"
            print(cmd)
            logging.info("cmd: " + cmd)

            subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
            with open(f"{output_file}.svg", "r") as f:
                svg_content = f.read()

            # fetch svg_seat_num from concert_data
            concert_data = app.db_concerts.find_one({"id": concert_id}, projection={"_id": 0})

            purchased_count = concert_input["seats"]["purchased"]

            # compare the svg_seat_num with the purchased_count, if svg_seat_num > purchased_count, abort, otherwise, generate svg. if svg_seat_num doesn't exist, generate svg
            if "svg_seat_num" in concert_data:
                if concert_data["svg_seat_num"] > purchased_count:
                    abort(400, "The number of seats in the svg file is larger than the number of purchased tickets.")
                    

            app.db_concerts.update_one({"id": concert_id}, {"$set": {"print_status": "PRINTED", "svg": svg_content, "svg_seat_num": purchased_count}})
            os.remove(input_file)
            os.remove(output_file + ".svg")

    except Exception as e:
        logging.error(e)
        app.db_concerts.update_one({"id": concert_id}, {"$set": {"print_status": "ERROR"}})

@hamilton_blueprint.route("/hamilton/concerts/<string:concert_id>", methods=["POST"])
def print_concert(concert_id):
    # get concert data
    concert_data = current_app.db_concerts.find_one({"id": concert_id}, projection={"_id": 0})
    # calculate purchased seats by count the number of tickets in db_users
    purchased_count = current_app.db_tickets.count_documents({"concert.id": concert_id})
    # svg payload
    svg_payload = {
        "id": concert_data["id"],
        "name": concert_data["name"],
        "date": concert_data["date"],
        "venue": concert_data["venue"],
        "seats": {
            "max": concert_data["capacity"],
            "purchased": purchased_count
        }
    }
    print("svg_payload: ", svg_payload)

    # compare the svg_seat_num with the purchased_count, if svg_seat_num > purchased_count, abort, otherwise, generate svg. if svg_seat_num doesn't exist, generate svg
    if "svg_seat_num" in concert_data:
        if concert_data["svg_seat_num"] > purchased_count:
            abort(400, "The number of seats in the svg file is larger than the number of purchased tickets.")

    concert_data = request.get_json()
    app = current_app._get_current_object()
    Thread(target=generate_concert, args=(svg_payload, app)).start()

    return jsonify({"status": "The asynchronous request was successfully started."}), 202