import json
import unittest
from unittest.mock import patch

from flask.testing import FlaskClient

from server import app


class TestServer(unittest.TestCase):
    """ Tests written by ChatGPT :) """

    def setUp(self):
        self.app = app.test_client()
        self.app.__class__ = FlaskClient

    @patch("server.SignatureVerifier.is_valid_request")
    def test_slash_command(self, mock_is_valid_request):
        mock_is_valid_request.return_value = True

        response = self.app.post("/slash-command", data={
            "text": "create",
            "user_id": "user1",
            "user_name": "username1",
            "response_url": "http://example.com"
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")

    @patch("server.SignatureVerifier.is_valid_request")
    def test_interactive(self, mock_is_valid_request):
        mock_is_valid_request.return_value = True

        payload = {
            "response_url": "http://example.com",
            "user": {"id": "user1", "username": "username1"},
            "actions": [{"action_id": "dummy_action", "value": "dummy_value", "type": "dummy_type"}]
        }

        response = self.app.post("/interactive", data={"payload": json.dumps(payload)})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")

if __name__ == '__main__':
    unittest.main()
