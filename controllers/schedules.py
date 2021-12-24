import json
from threading import Thread

import requests as requests

from util import slack_blocks


def handle_schedule_command():
    raise NotImplementedError


def list_schedules():
    raise NotImplementedError


def schedule_form_command(form_id, response_url):
    Thread(target=_send_schedule_form_response, kwargs=dict(form_id=form_id, response_url=response_url)).start()
    return


def _send_schedule_form_response(form_id, response_url):
    result = slack_blocks.reminder_select_block(form_id)
    requests.post(response_url, json.dumps(result))


def create_form_schedule_command(form_id, response_url):
    Thread(target=_create_schedule_and_respond, kwargs=dict(form_id=form_id, response_url=response_url)).start()
    return


def _create_schedule_and_respond(form_id, response_url):
    raise NotImplementedError
