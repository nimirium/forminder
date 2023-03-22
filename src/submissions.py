import json
from threading import Thread

import requests

from src import slack_ui_blocks
from src.models.form import SlackForm, Submission, SubmissionField
from src.utils import day_with_suffix


def submit_scheduled_form(form_id, user_id, payload, response_url):
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
    submission = Submission(form_id=form_id, user_id=user_id, fields=fields)

    Thread(target=_submit_form_and_respond, kwargs=dict(submission=submission, response_url=response_url)).start()
    return


def _submit_form_and_respond(submission, response_url):
    submission.save()
    result = slack_ui_blocks.text_response(":herb: The form was submitted :herb:")
    requests.post(response_url, json.dumps(result))


def view_submissions(form_id, user_id, response_url):
    Thread(target=_send_view_submissions_response,
           kwargs=dict(form_id=form_id, user_id=user_id, response_url=response_url)).start()


def _send_view_submissions_response(form_id, user_id, response_url):
    form = SlackForm.objects(id=form_id).first()
    blocks = [slack_ui_blocks.text_block_item(f":page_with_curl: {form.name} - submissions"),
              slack_ui_blocks.divider]
    submissions = Submission.objects(form_id=form_id, user_id=user_id).order_by('-created_at').limit(20)
    count = submissions.count()
    for i, submission in enumerate(submissions):
        formatted_date = submission.created_at.strftime("%A, %B {S}, %Y").replace(
            '{S}', day_with_suffix(submission.created_at.day))
        text = f""":spiral_calendar_pad: {formatted_date}"""
        for field in submission.fields:
            text += f"\nQ: {field.title}\nA: {field.value}"
        blocks.append(slack_ui_blocks.text_block_item(text))
        if i < count - 1:
            blocks.append(slack_ui_blocks.divider)
    response = dict(blocks=blocks)
    requests.post(response_url, json.dumps(response))


def submit_form_now(form_id, user_id, payload, response_url):
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
    submission = Submission(form_id=form_id, user_id=user_id, fields=fields)
    Thread(target=_submit_form_and_respond,
           kwargs=dict(submission=submission, response_url=response_url)).start()
