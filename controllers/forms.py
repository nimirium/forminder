import argparse
import json
from threading import Thread
from typing import List

import requests as requests

from util import slack_blocks
from models.form import SlackForm, SlackFormField
from mongoengine import Q

create_form_parser = argparse.ArgumentParser()
create_form_parser.add_argument("--form-name")
create_form_parser.add_argument("--text", action='append', nargs='?', default=[])
create_form_parser.add_argument("--text-multiline", action='append', nargs='?', default=[])
create_form_parser.add_argument("--public", default=False)


def create_form_command(user_id, user_name, command_args: List[str], response_url):
    if len(command_args) == 1:
        return slack_blocks.text_response(slack_blocks.form_create_help_text)
    params = create_form_parser.parse_args(command_args[1:])
    if not params.form_name:
        return slack_blocks.text_response(slack_blocks.form_create_help_text)
    if not params.text and not params.text_multiline:
        return slack_blocks.text_response(slack_blocks.form_create_help_text)

    fields = []
    for field_name in params.text:
        fields.append(SlackFormField(type='text', title=field_name))
    for field_name in params.text_multiline:
        fields.append(SlackFormField(type='text-multiline', title=field_name))
    form = SlackForm(
        user_id=user_id,
        user_name=user_name,
        form_name=params.form_name,
        fields=fields,
        public=params.public,
    )
    Thread(target=_create_form__save_and_respond, kwargs=dict(form=form, response_url=response_url)).start()
    return


def _create_form__save_and_respond(form, response_url):
    form.save()
    response = slack_blocks.text_response(f""":white_check_mark: Form ’{form.form_name}' was created
:information_source: Use “/ask-remind list forms” to see your forms
:arrow_right: Next, use “/ask-remind schedule” to schedule reminders to fill your form
""")
    requests.post(response_url, json.dumps(response))


def list_forms_command(user_id, response_url):
    Thread(target=_list_forms__fetch_and_respond, kwargs=dict(user_id=user_id, response_url=response_url)).start()
    return


def _list_forms__fetch_and_respond(user_id, response_url):
    response_text = ""
    for form in SlackForm.objects(Q(user_id=user_id) | Q(public=True)):
        fields_description = ', '.join([f"{f.title} ({f.type})" for f in form.fields])
        response_text += f""":page_with_curl: {form.form_name} 
Fields: {fields_description}
Not scheduled
Created by: {form.user_name}
"""
    response = slack_blocks.text_response(response_text)
    # return response
    requests.post(response_url, json.dumps(response))
