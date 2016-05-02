from xmlunittest import XmlTestCase
from warm_transfer_flask.models import ActiveCall


class BaseTest(XmlTestCase):

    def setUp(self):
        from warm_transfer_flask import app, db
        self.app = app
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.db = db
        self.client = self.app.test_client()
        ActiveCall.query.delete()
