from flask import Blueprint, jsonify, request, current_app, abort
from models.hamilton_ticket import HamiltonTicket
import uuid
import psutil
import os, threading, json
import subprocess
from threading import Thread
import logging



hamilton_blueprint = Blueprint("hamilton", __name__)


@hamilton_blueprint.route("/hamilton/test", methods=["GET"])
def test():
    return "Hamilton service is up and running!", 200

###### generate ticket ######

def generate_ticket(ticket_input, app):
    try:
        with app.app_context():
            ticket_id = ticket_input["id"]
            input_file = f"./temp/{ticket_id}_input.json"
            print("input_file: ", input_file)
            with open(input_file, "w") as f:
                json.dump(ticket_input, f)
            output_file = f"./temp/{ticket_id}_output"
            print("output_file: ", output_file)
            cmd = f"./bin/hamilton-v1.1.0-darwin-arm64 generate ticket --input {input_file} --output {output_file}"
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
        app.db_tickets.update_one({"id": ticket_id}, {"$set": {"print_status": "ERROR"}})



@hamilton_blueprint.route("/hamilton/tickets", methods=["POST"])
def print_ticket():
    ticket_data = request.get_json()
    app = current_app._get_current_object()
    Thread(target=generate_ticket, args=(ticket_data, app)).start()

    return jsonify({"status": "The asynchronous request was successfully started."}), 202


##### generat seat #####

def generate_concert(concert_input, app):
    try:
        with app.app_context():
            concert_id = concert_input["id"]
            logging.debug(msg=f"concert_id: {concert_id}")
            logging.debug(msg=f"concert_input: {concert_input}")
            input_file = f"./temp/{concert_id}_input.json"
            with open(input_file, "w") as f:
                json.dump(concert_input, f)
            output_file = f"./temp/{concert_id}_output"
            cmd = f"./bin/hamilton-v1.1.0-darwin-arm64 generate ticket --input {input_file} --output {output_file}"
            try:
                subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
                with open(f"{output_file}.svg", "r") as f:
                    svg_content = f.read()
                app.db_concerts.update_one({"id": concert_id}, {"$set": {"print_status": "PRINTED", "svg": svg_content}})
                os.remove(input_file)
                os.remove(output_file + ".svg")
            except subprocess.CalledProcessError as e:
                logging.error(e.output)
                app.db_concerts.update_one({"id": concert_id}, {"$set": {"print_status": "ERROR"}})
    except Exception as e:
        logging.error(e)
        app.db_concerts.update_one({"id": concert_id}, {"$set": {"print_status": "ERROR"}})

@hamilton_blueprint.route("/hamilton/concerts", methods=["POST"])
def print_concert():
    concert_data = request.get_json()
    app = current_app._get_current_object()
    Thread(target=generate_concert, args=(concert_data, app)).start()

    return jsonify({"status": "The asynchronous request was successfully started."}), 202