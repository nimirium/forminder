import argparse
import json
from threading import Thread
from typing import List

import requests as requests

from controllers.shared import list_form_blocks
from models.schedule import ScheduledEvent, FormSchedule
from util import slack_blocks, slack_actions
from models.form import SlackForm, SlackFormField
from util.slack_scheduler import delete_slack_scheduled_message

create_form_parser = argparse.ArgumentParser()
create_form_parser.add_argument("--form-name")
create_form_parser.add_argument("--text", action='append', nargs='?', default=[])
create_form_parser.add_argument("--text-multiline", action='append', nargs='?', default=[])
create_form_parser.add_argument("--public", default=False)


def create_form_command(user_id, user_name, command_args: List[str], response_url):
    if len(command_args) == 0:
        return slack_blocks.text_response(slack_blocks.form_create_help_text)
    params = create_form_parser.parse_args(command_args)
    if not params.form_name:
        return slack_blocks.text_response(slack_blocks.form_create_help_text)
    if not params.text and not params.text_multiline:
        return slack_blocks.text_response(slack_blocks.form_create_help_text)

    fields = []
    for field_name in params.text:
        fields.append(SlackFormField(type='text', title=field_name))
    for field_name in params.text_multiline:
        fields.append(SlackFormField(type='text-multiline', title=field_name))
    form_kwargs = dict(
        user_id=user_id,
        user_name=user_name,
        name=params.form_name,
        fields=fields,
        public=params.public,
    )
    Thread(target=_create_form__save_and_respond, kwargs=dict(form_kwargs=form_kwargs, response_url=response_url)).start()
    return


def _create_form__save_and_respond(form_kwargs, response_url):
    existing = SlackForm.objects(**form_kwargs)
    if existing:
        response = slack_blocks.text_response(":warning: This form already exists! :warning:")
        requests.post(response_url, json.dumps(response))
        return
    form = SlackForm(**form_kwargs)
    form.save()
    response = slack_blocks.text_response(f""":white_check_mark: Form ’{form.name}' was created
:information_source: Use “/forminder list forms” to see your forms
""")
    requests.post(response_url, json.dumps(response))


def list_forms_command(user_id, response_url):
    Thread(target=_list_forms__fetch_and_respond, kwargs=dict(user_id=user_id, response_url=response_url)).start()
    return


def _list_forms__fetch_and_respond(user_id, response_url):
    blocks = list_form_blocks(user_id)
    response = dict(blocks=blocks)
    requests.post(response_url, json.dumps(response))


def delete_form_command(form_id, user_id, response_url):
    Thread(target=_delete_form_and_respond,
           kwargs=dict(form_id=form_id, user_id=user_id, response_url=response_url)).start()
    return


def _delete_form_and_respond(form_id, user_id, response_url):
    form = SlackForm.objects(id=form_id).first()
    if not form:
        response = slack_blocks.text_response("Couldn't delete form because it does not exist")
        requests.post(response_url, json.dumps(response))
        return
    for schedule in FormSchedule.objects(form_id=str(form.id)):
        for event in ScheduledEvent.objects(schedule=schedule):
            if event.slack_message_id:
                delete_slack_scheduled_message(schedule.user_id, event.slack_message_id)
            event.delete()
        schedule.delete()
    form.delete()
    action_result = slack_blocks.text_block_item(f":white_check_mark: Deleted form '{form.name}'")
    form_blocks = list_form_blocks(user_id)
    response = dict(blocks=[action_result, slack_blocks.divider] + form_blocks)
    requests.post(response_url, json.dumps(response))


def fill_form_now_command(form_id, response_url):
    Thread(target=_send_fill_now_response, kwargs=dict(form_id=form_id, response_url=response_url)).start()
    return


def _send_fill_now_response(form_id, response_url):
    form = SlackForm.objects(id=form_id).first()
    blocks = []
    for block in slack_blocks.form_slack_blocks(form, action_id=slack_actions.SUBMIT_FORM_NOW):
        blocks.append(block)
    result = dict(blocks=blocks)
    requests.post(response_url, json.dumps(result))
