# tests/test_app.py

import unittest
from flask import json
from flask_testing import TestCase
from app import create_app, db
from models.ticket import Ticket
from models.user import User

class TestApp(TestCase):

    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['MONGODB_SETTINGS'] = {
            'db': 'test_db',
            'host': 'localhost',
            'port': 27017
        }
        return app