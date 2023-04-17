from os import environ
from flask import Flask
from pymongo import MongoClient
from views.routers import users_blueprint

def create_app(config_overrides=None):
    app = Flask(__name__)

    app.config['DOCUMENTDB_DATABASE_URI'] = environ.get("DOCUMENTDB_DATABASE_URI")
    if config_overrides:
        app.config.update(config_overrides)

    # Create MongoDB client
    client = MongoClient(app.config['DOCUMENTDB_DATABASE_URI'])
    app.db = client.ticketoverflow.users

    # Register the blueprint
    app.register_blueprint(users_blueprint, url_prefix='/api/v1')

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
