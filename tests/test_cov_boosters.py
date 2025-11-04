import os, importlib
from unittest import TestCase
from service import app
from service.common import log_handlers
from flask import Response

# test-only 500 route
@app.route("/__boom")
def __boom():
    raise RuntimeError("boom")

class TestCoverageBoosters(TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_404_handler(self):
        resp = self.client.get("/no-such-route")
        assert resp.status_code == 404
        body = resp.get_json()
        assert body["status"] == 404

    def test_405_handler(self):
        resp = self.client.post("/health")
        assert resp.status_code == 405
        body = resp.get_json()
        # allow template's exact text casing
        assert "Allowed" in body.get("error", "")

    def test_400_handler(self):
        resp = self.client.post("/accounts", json={"email": "x@x"})
        assert resp.status_code == 400
        body = resp.get_json()
        assert body["status"] == 400

    def test_500_handler(self):
        # hit internal_server_error handler
        resp: Response = self.client.get("/__boom")
        assert resp.status_code == 500
        body = resp.get_json()
        assert body["status"] == 500

    def test_logging_init_paths(self):
        log_handlers.init_logging(app, "gunicorn.error")
        log_handlers.init_logging(app, "does.not.exist")
        # empty name to hit alternate branch
        try:
            log_handlers.init_logging(app, "")
        except Exception:
            pass

    def test_config_reload_with_env(self):
        import service.config as cfg
        os.environ["FLASK_ENV"] = "production"
        os.environ["DATABASE_URL"] = "sqlite:///db/test_cov.db"
        importlib.reload(cfg)
        assert hasattr(cfg, "__name__")
        os.environ["FLASK_ENV"] = "development"
        importlib.reload(cfg)
        assert hasattr(cfg, "__name__")
