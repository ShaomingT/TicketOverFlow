from os import environ
from flask import Flask
from pymongo import MongoClient
from views.routers import concerts_blueprint
import logging

def create_app():
    app = Flask(__name__)
    app.config['DOCUMENTDB_DATABASE_URI'] = environ.get("DOCUMENTDB_DATABASE_URI")
    app.config['SERVICE_USER_URL'] = environ.get("SERVICE_USER_URL")
    app.config['SERVICE_CONCERT_URL'] = environ.get("SERVICE_CONCERT_URL")
    app.config['SERVICE_TICKET_URL'] = environ.get("SERVICE_TICKET_URL")

    # Create MongoDB client
    client = MongoClient(app.config['DOCUMENTDB_DATABASE_URI'])
    app.db_users = client.ticketoverflow.users
    app.db_tickets = client.ticketoverflow.tickets
    app.db_concerts = client.ticketoverflow.concerts

    # Register the blueprint
    app.register_blueprint(concerts_blueprint, url_prefix='/api/v1')

    return app

def wsgi_app(environ, start_response):
    app = create_app()
    return app(environ, start_response)

if __name__ == '__main__':
    app = create_app()
    app.logger.setLevel(logging.DEBUG)

    app.config['SERVICE_USER_URL'] = "SERVICE_USER_URL"
    app.config['SERVICE_CONCERT_URL'] = "http://127.0.0.1:5000/api/v1/tickets"
    app.config['SERVICE_TICKET_URL'] = "SERVICE_TICKET_URL"

    app.config['DOCUMENTDB_DATABASE_URI'] = "mongodb://root:example@localhost:27017/"
    client = MongoClient(app.config['DOCUMENTDB_DATABASE_URI'])
    app.logger.info(f"{app.config}")
    app.db_users = client.ticketoverflow.users
    app.db_tickets = client.ticketoverflow.tickets
    app.db_concerts = client.ticketoverflow.concerts

    app.app_context().push()
    app.run(debug=True)
