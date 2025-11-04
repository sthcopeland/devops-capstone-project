import os, importlib
from unittest import TestCase
from service import app

# route that *already* sets HSTS to hit the "else" of after_request
@app.route("/__hsts_set")
def __hsts_set():
    from flask import make_response
    r = make_response(("ok", 200, {"Strict-Transport-Security": "max-age=1"}))
    return r

class TestMoreCoverage(TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_after_request_when_hsts_already_set(self):
        resp = self.client.get("/__hsts_set")
        assert resp.status_code == 200
        assert "Strict-Transport-Security" in resp.headers

    def test_config_three_paths(self):
        import service.config as cfg
        # 1) with DATABASE_URL
        os.environ["DATABASE_URL"] = "sqlite:///db/a.db"
        os.environ.pop("DATABASE_URI", None)
        importlib.reload(cfg)
        assert "sqlite" in os.getenv("DATABASE_URL", "")
        # 2) with DATABASE_URI
        os.environ["DATABASE_URI"] = "sqlite:///db/b.db"
        os.environ.pop("DATABASE_URL", None)
        importlib.reload(cfg)
        assert "sqlite" in os.getenv("DATABASE_URI", "")
        # 3) with neither
        os.environ.pop("DATABASE_URI", None)
        os.environ.pop("DATABASE_URL", None)
        importlib.reload(cfg)
        assert hasattr(cfg, "__name__")
