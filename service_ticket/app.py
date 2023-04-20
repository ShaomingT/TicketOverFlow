from os import environ
from flask import Flask
from pymongo import MongoClient
from views.routers import tickets_blueprint



def create_app():
    app = Flask(__name__)

    app.config['DOCUMENTDB_DATABASE_URI'] = environ.get("DOCUMENTDB_DATABASE_URI")


    # Create MongoDB client
    client = MongoClient(app.config['DOCUMENTDB_DATABASE_URI'])
    app.db = client.ticketoverflow.users

    # Register the blueprint
    app.register_blueprint(tickets_blueprint, url_prefix='/api/v1')

    return app


def wsgi_app(environ, start_response):
    app = create_app()
    return app(environ, start_response)

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)