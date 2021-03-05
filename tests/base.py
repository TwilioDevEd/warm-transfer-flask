from unittest import TestCase

from warm_transfer_flask import app, db


class BaseTestCase(TestCase):
    def setUp(self):
        self.client = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
