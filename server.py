import json
import os
import shlex

import requests
from flask import Flask, request, Response, jsonify, render_template
from slack_sdk.signature import SignatureVerifier

from src import submissions, forms, schedules, slack_actions, slack_ui_blocks
from src.models.connect import connect_to_mongo

app = Flask(__name__)
connect_to_mongo()
slack_verifier = SignatureVerifier(os.environ['SIGNING_SECRET'])

SLACK_CLIENT_ID = os.environ.get("SLACK_CLIENT_ID")
SLACK_CLIENT_SECRET = os.environ.get("SLACK_CLIENT_SECRET")
SLACK_OAUTH_URL = "https://slack.com/api/oauth.v2.access"
SLACK_USER_INFO_URL = "https://slack.com/api/users.info"


def verify_slack_request(func, *args, **kwargs):
    def wrapper():
        if slack_verifier.is_valid_request(request.get_data(), request.headers):
            return func(*args, **kwargs)
        return Response(status=401)

    wrapper.__name__ = func.__name__

    return wrapper


@app.route('/')
def index():
    return render_template('sign-in.html', SLACK_CLIENT_ID=SLACK_CLIENT_ID)


@app.route('/oauth2', methods=['GET'])
def oauth_callback():
    code = request.args.get('code')

    # Exchange the authorization code for an access token
    payload = {
        'client_id': SLACK_CLIENT_ID,
        'client_secret': SLACK_CLIENT_SECRET,
        'code': code
    }
    response = requests.post(SLACK_OAUTH_URL, data=payload)
    response_data = response.json()

    # Fetch user information
    auth_token = response_data['authed_user']['access_token']
    headers = {'Authorization': f"Bearer {auth_token}"}
    user_response = requests.get(SLACK_USER_INFO_URL, headers=headers)
    user_data = user_response.json()

    # Process user data as needed
    # For example, you can store the user's information in your database

    # Return a JSON response with user data
    return jsonify(user_data)

@app.route("/slash-command", methods=['POST'])
@verify_slack_request
def slack_webhook():
    user_id = request.form['user_id']
    user_name = request.form['user_name']
    response_url = request.form['response_url']
    command_text = (request.form['text'] or '').replace("”", '"').replace("“", '"')
    args = shlex.split(command_text)
    result = None
    if len(args) < 1:
        result = slack_ui_blocks.help_text_block
    elif args[0] == "create":
        result = forms.create_form_command(user_id, user_name, args[1:], response_url)
    elif args[0] == "list":
        result = forms.list_forms_command(user_id, response_url)
    if result:
        return Response(response=json.dumps(result), status=200, mimetype="application/json")
    return Response(status=200, mimetype="application/json")


@app.route("/interactive", methods=['POST'])
@verify_slack_request
def slack_interactive_endpoint():
    payload = json.loads(request.form['payload'])
    response_url = payload['response_url']
    user_id = payload['user']['id']
    user_name = payload['user']['username']
    result = None
    for action in payload['actions']:
        action_id = action['action_id']
        if action_id in (slack_actions.FORM_WEEKDAYS, slack_actions.FORM_TIME) or action.get('type') == 'static_select':
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
