from unittest import TestCase
from service import app

class TestSecurity(TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_security_headers_present(self):
        resp = self.client.get("/")
        # Strict-Transport-Security should exist
        assert "Strict-Transport-Security" in resp.headers
        # Content-Security-Policy should exist
        assert "Content-Security-Policy" in resp.headers

    def test_cors_header_present(self):
        resp = self.client.get("/", headers={"Origin": "http://example.com"})
        # Access-Control-Allow-Origin should be set (simple check)
        assert "Access-Control-Allow-Origin" in resp.headers
