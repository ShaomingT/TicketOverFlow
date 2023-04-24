from os import environ
from flask import Flask
from views.routers import users_blueprint
from flask_sqlalchemy import SQLAlchemy
from models import db
import logging


def create_app(config_overrides=None):
    app = Flask(__name__)

    gunicorn_error_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers.extend(gunicorn_error_logger.handlers)
    app.logger.setLevel(logging.DEBUG)

    app.config['SQLALCHEMY_DATABASE_URI'] = environ.get("SQLALCHEMY_DATABASE_URI")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # print all the env variables
    for key, value in environ.items():
        print(f"{key}={value}")
    # print all env variables in logger error
    for key, value in environ.items():
        app.logger.info(f"{key}={value}")
    if config_overrides:
        app.config.update(config_overrides)

    # Initialize the database
    db.init_app(app)

    # Create the database tables.
    with app.app_context():
        db.create_all()
        db.session.commit()

    # Register the blueprint
    app.register_blueprint(users_blueprint, url_prefix='/api/v1')
    return app


def wsgi_app(environ, start_response):
    app = create_app()
    return app(environ, start_response)


if __name__ == '__main__':
    # Override the SQLALCHEMY_DATABASE_URI configuration for the development environment.
    # config_overrides = {
    #     'SQLALCHEMY_DATABASE_URI': 'postgresql://postgres:postgres@localhost:5432/ticketoverflow'
    # }
    config_overrides = {
        'SQLALCHEMY_DATABASE_URI': "postgresql://postgres:postgres@terraform-20230424152844100400000001.cvwf3fikf7zu.us-east-1.rds.amazonaws.com:5432/ticketoverflow",
        'SERVICE_HAMILTON_URL': "https://h4s4anelr4.execute-api.us-east-1.amazonaws.com/prod/hamilton"
    }
    # Create the Flask application instance with the configuration overrides.
    app = create_app(config_overrides=config_overrides)

    app.run(debug=True)
#a
