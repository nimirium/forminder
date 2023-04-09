import json
from threading import Thread

import requests

from src import slack_ui_blocks
from src.models.form import SlackForm, Submission, SubmissionField
from src.slack_api.slack_user import SlackUser


def submit_scheduled_form(form_id, user: SlackUser, payload, response_url):
    fields = []
    inputs = [x for x in payload['message']['blocks'] if x['type'] == 'input']
    questions = {}
    for input_item in inputs:
        block_id = input_item['block_id']
        question = input_item['label']['text']
        questions[block_id] = question
    for block_id, form_field in payload['state']['values'].items():
        val = list(form_field.values())[0]['value']
        title = questions[block_id]
        fields.append(SubmissionField(
            title=title,
            value=val,
        ))
    submission = Submission(form_id=form_id, user_id=user.id, user_name=user.username, fields=fields)

    Thread(target=submit_form_and_respond, kwargs=dict(submission=submission, response_url=response_url)).start()
    return


def submit_form_and_respond(submission, response_url):
    submission.save()
    result = slack_ui_blocks.text_response(":herb: The form was submitted :herb:")
    requests.post(response_url, json.dumps(result))


def submit_form_now(form_id, user: SlackUser, payload, response_url):
    fields = []
    form = SlackForm.objects(id=form_id).first()
    for slack_form in payload['state']['values'].values():
        for field_id, item in slack_form.items():
            if item['type'] == 'static_select':
                val = item['selected_option']['value']
            else:
                val = item['value']
            field = [x for x in form.fields if str(x.id) == field_id][0]
            fields.append(SubmissionField(
                title=field.title,
                value=val,
            ))
    submission = Submission(form_id=form_id, user_id=user.id, user_name=user.username, fields=fields)
    Thread(target=submit_form_and_respond,
           kwargs=dict(submission=submission, response_url=response_url)).start()
