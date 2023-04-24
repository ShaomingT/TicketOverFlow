from os import environ
from flask import Flask
from views.routers import concerts_blueprint
from models import db
import logging


def create_app(config_overrides=None):
    app = Flask(__name__)

    gunicorn_error_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers.extend(gunicorn_error_logger.handlers)
    app.logger.setLevel(logging.DEBUG)

    app.config['SERVICE_USER_URL'] = environ.get("SERVICE_USER_URL")
    app.config['SERVICE_CONCERT_URL'] = environ.get("SERVICE_CONCERT_URL")
    app.config['SERVICE_TICKET_URL'] = environ.get("SERVICE_TICKET_URL")
    app.config['SERVICE_HAMILTON_URL'] = environ.get("SERVICE_HAMILTON_URL")

    app.config['SQLALCHEMY_DATABASE_URI'] = environ.get("SQLALCHEMY_DATABASE_URI")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    if config_overrides:
        app.config.update(config_overrides)

    # Initialize the database
    db.init_app(app)

    # Create the database tables.
    with app.app_context():
        db.create_all()
        db.session.commit()

    # Register the blueprint
    app.register_blueprint(concerts_blueprint, url_prefix='/api/v1')
    return app


def wsgi_app(environ, start_response):
    app = create_app()
    return app(environ, start_response)


if __name__ == '__main__':
    # Override the SQLALCHEMY_DATABASE_URI configuration for the development environment.
    config_overrides = {
        'SQLALCHEMY_DATABASE_URI': 'postgresql://postgres:postgres@localhost:5432/ticketoverflow'
    }
    # Create the Flask application instance with the configuration overrides.
    app = create_app(config_overrides=config_overrides)
    app.logger.setLevel(logging.DEBUG)

    app.config['SERVICE_USER_URL'] = environ.get("SERVICE_USER_URL")
    app.config['SERVICE_CONCERT_URL'] = "http://127.0.0.1:5000/api/v1/tickets"
    app.config['SERVICE_TICKET_URL'] = environ.get("SERVICE_TICKET_URL")
    app.config['SERVICE_HAMILTON_URL'] = "http://127.0.0.1:6666/api/v1/hamilton"

    app.app_context().push()
    app.run(debug=True, port=7777)
#a