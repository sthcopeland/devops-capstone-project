from unittest import TestCase
from service import app, models
from service.models import Account, db

class TestCovSqueeze(TestCase):
    def setUp(self):
        self.client = app.test_client()
        with app.app_context():
            db.session.query(Account).delete()
            db.session.commit()

    def test_models_init_db_idempotent(self):
        models.init_db(app)
        models.init_db(app)

    def test_account_deserialize_minimal_valid(self):
        a = Account()
        a.deserialize({"name": "Mini", "email": "mini@example.com", "address": "1 St"})
        assert a.name and a.email and a.address
