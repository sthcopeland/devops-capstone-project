from unittest import TestCase
from service import app
from service.models import Account, db

class TestModelExtra(TestCase):
    def setUp(self):
        self.client = app.test_client()
        with app.app_context():
            db.session.query(Account).delete()
            db.session.commit()

    def test_repr_serialize_and_finders(self):
        with app.app_context():
            acct = Account(name="Test User", email="test@example.com", address="123 Any St")
            acct.create()
            # __repr__ / __str__
            r = repr(acct)
            assert "Account" in r or "test@example.com" in r

            # serialize() uses all fields
            data = acct.serialize()
            assert data["id"] == acct.id
            assert data["name"] == "Test User"
            assert data["email"] == "test@example.com"
            assert data["address"] == "123 Any St"

            # find(id)
            got = Account.find(acct.id)
            assert got is not None and got.id == acct.id

            # find_by_name (template provides this; already used in other tests—hit again)
            results = Account.find_by_name("Test User")
            assert any(a.id == acct.id for a in results)
