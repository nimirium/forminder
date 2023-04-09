import json
import logging
import unittest
from unittest import mock
from unittest.mock import patch, MagicMock

from mongoengine import connect, disconnect

from src import slack_ui_blocks
from src.constants import SLASH_COMMAND
from src.forms import create_form_command, create_form__save_and_respond, delete_form_and_respond, \
    send_fill_now_response
from src.models.form import SlackForm


class TestForms(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # connect to the test database
        disconnect()
        connect('testdb', host='mongomock://localhost')
        logging.info("connected to mongo: testdb")

    @classmethod
    def tearDownClass(cls):
        # disconnect from the test database
        disconnect()

    def setUp(self):
        self.old_save = None
        # clear the SlackForm collection before each test
        SlackForm.objects.delete()


    def tearDown(self) -> None:
        if self.old_save:
            SlackForm.save = self.old_save

    def test_create_form_command_with_no_args(self):
        result = create_form_command("user_id", "user_name", [], "response_url")
        self.assertEqual(result, slack_ui_blocks.text_response(slack_ui_blocks.form_create_help_text))

    def test_create_form_command_with_no_form_name(self):
        result = create_form_command("user_id", "user_name", ["--text-field", "field1"], "response_url")
        self.assertEqual(result, slack_ui_blocks.text_response(slack_ui_blocks.form_create_help_text))

    def test_create_form_command_with_no_fields(self):
        result = create_form_command("user_id", "user_name", ["--form-name", "form1"], "response_url")
        self.assertEqual(result, slack_ui_blocks.text_response(slack_ui_blocks.form_create_help_text))

    def test_create_form_command_with_text_field(self):
        with patch("src.forms.Thread") as mock_thread:
            result = create_form_command("user_id", "user_name", ["--form-name", "form1", "--text-field", "field1"], "response_url")
            mock_thread.assert_called_once()
            args, kwargs = mock_thread.call_args
            self.assertEqual(args, ())
            self.assertEqual(kwargs["kwargs"]["form_kwargs"]["name"], "form1")
            self.assertEqual(kwargs["kwargs"]["form_kwargs"]["fields"][0].type, "text")
            self.assertEqual(kwargs["kwargs"]["form_kwargs"]["fields"][0].title, "field1")

    def test_create_form_command_with_multiline_field(self):
        with patch("src.forms.Thread") as mock_thread:
            result = create_form_command("user_id", "user_name", ["--form-name", "form1", "--multiline-field", "field1"], "response_url")
            mock_thread.assert_called_once()
            args, kwargs = mock_thread.call_args
            self.assertEqual(args, ())
            self.assertEqual(kwargs["kwargs"]["form_kwargs"]["name"], "form1")
            self.assertEqual(kwargs["kwargs"]["form_kwargs"]["fields"][0].type, "text-multiline")
            self.assertEqual(kwargs["kwargs"]["form_kwargs"]["fields"][0].title, "field1")

    def test_create_form_command_with_select_field(self):
        with patch("src.forms.Thread") as mock_thread:
            result = create_form_command("user_id", "user_name", ["--form-name", "form1", "--select-field", "field1:option1,option2"], "response_url")
            mock_thread.assert_called_once()
            args, kwargs = mock_thread.call_args
            self.assertEqual(args, ())
            self.assertEqual(kwargs["kwargs"]["form_kwargs"]["name"], "form1")
            self.assertEqual(kwargs["kwargs"]["form_kwargs"]["fields"][0].type, "select")
            self.assertEqual(kwargs["kwargs"]["form_kwargs"]["fields"][0].title, "field1")
            self.assertEqual(kwargs["kwargs"]["form_kwargs"]["fields"][0].options, ["option1", "option2"])

    def test_create_form_command_with_invalid_select_field(self):
        result = create_form_command("user_id", "user_name", ["--form-name", "form1", "--select-field", "field1"], "response_url")
        self.assertEqual(result, slack_ui_blocks.text_response(slack_ui_blocks.form_create_help_text))


    @patch("src.forms.requests.post")
    @patch.object(SlackForm, "objects", return_value=[])
    def test_create_form_save_and_respond(self, mock_objects, mock_post):
        form_kwargs = dict(
            user_id="user1",
            user_name="user_name",
            name="form1",
            fields=[],
        )
        response_url = "http://example.com"
        self.old_save = SlackForm.save
        SlackForm.save = MagicMock()
        create_form__save_and_respond(form_kwargs, response_url)
        SlackForm.save.assert_called_once()
        expected_response = slack_ui_blocks.text_response(f""":white_check_mark: Form ’{form_kwargs['name']}' was created
:information_source: Use “/{SLASH_COMMAND} list” to see your forms
""")
        mock_post.assert_called_once_with(response_url, json.dumps(expected_response))


    @patch("src.forms.requests.post")
    def test_delete_form_and_respond(self, mock_post):
        # create a SlackForm instance to delete
        form = SlackForm(user_id="user1", user_name="user_name", name="form1", fields=[])
        form.save()

        # call the delete_form_and_respond function
        delete_form_and_respond(str(form.id), "user1", "response_url")

        # check that the form and its schedules and events are deleted
        self.assertIsNone(SlackForm.objects(id=str(form.id)).first())

        # check that the response message is sent
        mock_post.assert_called_once()

    @mock.patch("src.forms.requests.post")
    def test_send_fill_now_response(self, mock_post):
        form = SlackForm.objects.create(name="form1")
        response_url = "http://example.com"

        send_fill_now_response(str(form.id), response_url)

        # assert the type and text of the first block
        expected_block_1 = {
            'type': 'section',
            'text': {
                'type': 'mrkdwn',
                'text': 'form1'
            }
        }
        self.assertEqual(mock_post.call_args_list[0].args[0], response_url)
        self.assertDictEqual(json.loads(mock_post.call_args_list[0].args[1])['blocks'][0], expected_block_1)

        # assert the type, value, and action_id of the button element
        expected_element = {
            'type': 'button',
            'text': {
                'type': 'plain_text',
                'text': 'Submit',
                'emoji': True
            },
            'value': mock.ANY,
            'action_id': 'submit-form-now'
        }
        self.assertEqual(json.loads(mock_post.call_args_list[0].args[1])['blocks'][1]['type'], 'actions')
        self.assertEqual(json.loads(mock_post.call_args_list[0].args[1])['blocks'][1]['elements'][0]['type'], 'button')
        self.assertEqual(json.loads(mock_post.call_args_list[0].args[1])['blocks'][1]['elements'][0]['text'],
                         expected_element['text'])
        self.assertEqual(json.loads(mock_post.call_args_list[0].args[1])['blocks'][1]['elements'][0]['action_id'],
                         expected_element['action_id'])