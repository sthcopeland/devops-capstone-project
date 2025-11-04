import importlib, types
from unittest import TestCase, mock

class TestInitFailPath(TestCase):
    def test_init_db_failure_path(self):
        import service
        # patch models.init_db to raise once
        with mock.patch("service.models.init_db", side_effect=RuntimeError("boom")):
            # patch sys.exit so except block doesn't terminate tests
            with mock.patch("service.sys.exit", lambda code: None):
                importlib.reload(service)
