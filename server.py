import json
import shlex

from flask import Flask, request, Response

from controllers import forms, schedules, submissions
from util import slack_blocks, slack_actions
from models.connect import connect_to_mongo

app = Flask(__name__)
connect_to_mongo()


@app.route("/slack-webhook", methods=['POST'])
def slack_webhook():
    user_id = request.form['user_id']
    user_name = request.form['user_name']
    response_url = request.form['response_url']
    command_text = (request.form['text'] or '').replace("”", '"').replace("“", '"')
    args = shlex.split(command_text)
    result = None
    if len(args) < 2:
        result = slack_blocks.help_text_block
    elif args[0] == "create" and args[1] == "form":
        result = forms.create_form_command(user_id, user_name, args[2:], response_url)
    elif args[0] == "list" and args[1] == "forms":
        result = forms.list_forms_command(user_id, response_url)
    if result:
        return Response(response=json.dumps(result), status=200, mimetype="application/json")
    return Response(status=200, mimetype="application/json")


@app.route("/slack-interactive-endpoint", methods=['POST'])
def slack_interactive_endpoint():
    payload = json.loads(request.form['payload'])
    response_url = payload['response_url']
    user_id = payload['user']['id']
    user_name = payload['user']['username']
    result = None
    for action in payload['actions']:
        action_id = action['action_id']
        if action_id in (slack_actions.FORM_WEEKDAYS, slack_actions.FORM_TIME) or action['type'] == 'static_select':
            return Response(status=200, mimetype="application/json")
        value = action['value']
        if action_id == slack_actions.DELETE_FORM:
            result = forms.delete_form_command(value, user_id, response_url)
        elif action_id == slack_actions.FILL_FORM_NOW:
            result = forms.fill_form_now_command(value, response_url)
        elif action_id == slack_actions.SCHEDULE_FORM:
            result = schedules.schedule_form_command(value, response_url)
        elif action_id == slack_actions.CREATE_FORM_SCHEDULE:
            schedule_form_state = payload['state']['values']
            result = schedules.create_form_schedule_command(value, user_id, user_name, schedule_form_state, response_url)
        elif action_id == slack_actions.DELETE_SCHEDULE:
            result = schedules.delete_schedule_command(value, user_id, response_url)
        elif action_id == slack_actions.SUBMIT_FORM_SCHEDULED:
            result = submissions.submit_scheduled_form(value, user_id, payload, response_url)
        elif action_id == slack_actions.SUBMIT_FORM_NOW:
            result = submissions.submit_form_now(value, user_id, payload, response_url)
        elif action_id == slack_actions.VIEW_FORM_SUBMISSIONS:
            result = submissions.view_submissions(value, user_id, response_url)
    if result:
        return Response(response=json.dumps(result), status=200, mimetype="application/json")
    return Response(status=200, mimetype="application/json")
