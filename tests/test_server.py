import json
import unittest
from unittest.mock import patch

from flask.testing import FlaskClient

from server import app
from util import slack_actions


class TestServer(unittest.TestCase):
    """ Tests written with the help of ChatGPT :) """

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

    @patch("server.SignatureVerifier.is_valid_request")
    @patch("server.forms.create_form_command")
    def test_create_form_command_called(self, mock_create_form_command, mock_is_valid_request):
        mock_is_valid_request.return_value = True
        mock_create_form_command.return_value = {"text": "Form created"}

        response = self.app.post("/slash-command", data={
            "text": 'create --text="Question 1" --select="Color:red,blue,yellow"',
            "user_id": "user1",
            "user_name": "username1",
            "response_url": "http://example.com"
        })

        mock_create_form_command.assert_called_once_with(
            "user1", "username1", ['--text=Question 1', '--select=Color:red,blue,yellow'], "http://example.com"
        )
        self.assertEqual(response.status_code, 200)


    @patch("server.SignatureVerifier.is_valid_request")
    @patch("server.forms.list_forms_command")
    def test_list_forms_command_called(self, mock_list_forms_command, mock_is_valid_request):
        mock_is_valid_request.return_value = True
        mock_list_forms_command.return_value = {"text": "Listing forms"}

        response = self.app.post("/slash-command", data={
            "text": "list",
            "user_id": "user1",
            "user_name": "username1",
            "response_url": "http://example.com"
        })

        mock_list_forms_command.assert_called_once_with("user1", "http://example.com")
        self.assertEqual(response.status_code, 200)


    def create_payload(self, action_id, value=None, action_type=None, state=None):
        payload = {
            "response_url": "http://example.com",
            "user": {"id": "user1", "username": "username1"},
            "actions": [{"action_id": action_id}]
        }

        if value is not None:
            payload["actions"][0]["value"] = value

        if action_type is not None:
            payload["actions"][0]["type"] = action_type

        if state is not None:
            payload["state"] = {"values": state}

        return payload

    def post_interactive(self, payload):
        return self.app.post("/interactive", data={"payload": json.dumps(payload)})

    @patch("server.SignatureVerifier.is_valid_request")
    @patch("server.forms.delete_form_command")
    def test_interactive_delete_form(self, mock_delete_form_command, mock_is_valid_request):
        mock_is_valid_request.return_value = True
        mock_delete_form_command.return_value = {"text": "Form deleted"}
        payload = self.create_payload(slack_actions.DELETE_FORM, "form1")
        response = self.post_interactive(payload)
        mock_delete_form_command.assert_called_once_with("form1", "user1", "http://example.com")
        self.assertEqual(response.status_code, 200)


    @patch("server.SignatureVerifier.is_valid_request")
    @patch("server.forms.fill_form_now_command")
    def test_interactive_fill_form_now(self, mock_fill_form_now_command, mock_is_valid_request):
        mock_is_valid_request.return_value = True
        mock_fill_form_now_command.return_value = {"text": "Form deleted"}
        payload = self.create_payload(slack_actions.FILL_FORM_NOW, "form1")
        response = self.post_interactive(payload)
        mock_fill_form_now_command.assert_called_once_with("form1", "http://example.com")
        self.assertEqual(response.status_code, 200)


    @patch("server.SignatureVerifier.is_valid_request")
    @patch("server.schedules.schedule_form_command")
    def test_interactive_schedule_form(self, mock_schedule_form_command, mock_is_valid_request):
        mock_is_valid_request.return_value = True
        mock_schedule_form_command.return_value = {"text": "Form deleted"}
        payload = self.create_payload(slack_actions.SCHEDULE_FORM, "form1")
        response = self.post_interactive(payload)
        mock_schedule_form_command.assert_called_once_with("form1", "http://example.com")
        self.assertEqual(response.status_code, 200)


    @patch("server.SignatureVerifier.is_valid_request")
    @patch("server.schedules.create_form_schedule_command")
    def test_interactive_create_form_schedule(self, mock_create_form_schedule_command, mock_is_valid_request):
        mock_is_valid_request.return_value = True
        mock_create_form_schedule_command.return_value = {"text": "Form deleted"}
        payload = self.create_payload(slack_actions.CREATE_FORM_SCHEDULE, "form1", state={"state1": "val1"})
        response = self.post_interactive(payload)
        mock_create_form_schedule_command.assert_called_once_with("form1", "user1", "username1", {"state1": "val1"}, "http://example.com")
        self.assertEqual(response.status_code, 200)


    @patch("server.SignatureVerifier.is_valid_request")
    @patch("server.schedules.delete_schedule_command")
    def test_interactive_delete_schedule(self, mock_delete_schedule_command, mock_is_valid_request):
        mock_is_valid_request.return_value = True
        mock_delete_schedule_command.return_value = {"text": "Form deleted"}
        payload = self.create_payload(slack_actions.DELETE_SCHEDULE, "form1")
        response = self.post_interactive(payload)
        mock_delete_schedule_command.assert_called_once_with("form1", "user1", "http://example.com")
        self.assertEqual(response.status_code, 200)


    @patch("server.SignatureVerifier.is_valid_request")
    @patch("server.submissions.submit_scheduled_form")
    def test_interactive_submit_scheduled_form(self, mock_submit_scheduled_form, mock_is_valid_request):
        mock_is_valid_request.return_value = True
        mock_submit_scheduled_form.return_value = {"text": "Form deleted"}
        payload = self.create_payload(slack_actions.SUBMIT_FORM_SCHEDULED, "form1")
        response = self.post_interactive(payload)
        mock_submit_scheduled_form.assert_called_once_with('form1', 'user1', payload, 'http://example.com')
        self.assertEqual(response.status_code, 200)


    @patch("server.SignatureVerifier.is_valid_request")
    @patch("server.submissions.submit_form_now")
    def test_interactive_submit_form_now(self, mock_submit_form_now, mock_is_valid_request):
        mock_is_valid_request.return_value = True
        mock_submit_form_now.return_value = {"text": "Form deleted"}
        payload = self.create_payload(slack_actions.SUBMIT_FORM_NOW, "form1")
        response = self.post_interactive(payload)
        mock_submit_form_now.assert_called_once_with('form1', 'user1', payload, 'http://example.com')
        self.assertEqual(response.status_code, 200)


    @patch("server.SignatureVerifier.is_valid_request")
    @patch("server.submissions.view_submissions")
    def test_interactive_view_submissions(self, mock_view_submissions, mock_is_valid_request):
        mock_is_valid_request.return_value = True
        mock_view_submissions.return_value = {"text": "Form deleted"}
        payload = self.create_payload(slack_actions.VIEW_FORM_SUBMISSIONS, "form1")
        response = self.post_interactive(payload)
        mock_view_submissions.assert_called_once_with('form1', 'user1', 'http://example.com')
        self.assertEqual(response.status_code, 200)


    @patch("server.SignatureVerifier.is_valid_request")
    def test_interactive_static_select(self, mock_is_valid_request):
        mock_is_valid_request.return_value = True

        payload = {
            "response_url": "http://example.com",
            "user": {"id": "user1", "username": "username1"},
            "actions": [{"action_id": "dummy_action", "value": "dummy_value", "type": "static_select"}]
        }

        response = self.app.post("/interactive", data={"payload": json.dumps(payload)})

        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
