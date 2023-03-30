import json
import logging
import os
import shlex
from datetime import timedelta

import requests
from flask import Flask, request, Response, jsonify, render_template, session, redirect, url_for
from flask_session import Session
from slack_sdk.signature import SignatureVerifier
from pymongo import MongoClient

from src import submissions, forms, schedules, constants, slack_ui_blocks
from src.constants import SLASH_COMMAND
from src.models.connect import connect_to_mongo
from src.models.form import Submission, SlackForm

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

SLACK_CLIENT_ID = os.environ["SLACK_CLIENT_ID"]
SLACK_CLIENT_SECRET = os.environ["SLACK_CLIENT_SECRET"]
SLACK_OAUTH_URL = "https://slack.com/api/oauth.v2.access"
SLACK_USER_INFO_URL = "https://slack.com/api/users.info"
DOMAIN = os.environ['DOMAIN']
MONGO_DB_URL = os.environ['MONGO_DB_URL']
MONGO_DB_NAME = os.environ['MONGO_DB_NAME']
SESSION_COOKIE_NAME = 'session'

connect_to_mongo()
pymongo_client = MongoClient(MONGO_DB_URL)

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ['SESSION_KEY']  # Replace with your secret key
app.config['SESSION_TYPE'] = 'mongodb'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_NAME'] = SESSION_COOKIE_NAME
app.config['SESSION_MONGODB'] = pymongo_client
app.config['SESSION_MONGODB_DB'] = MONGO_DB_NAME

Session(app)
slack_verifier = SignatureVerifier(os.environ['SIGNING_SECRET'])


def verify_slack_request(func, *args, **kwargs):
    def wrapper():
        if slack_verifier.is_valid_request(request.get_data(), request.headers):
            return func(*args, **kwargs)
        return Response(status=401)

    wrapper.__name__ = func.__name__
    return wrapper


def user_logged_in(func, *args, **kwargs):
    def wrapper():
        if request.args.get('code') and 'access_token' not in session or 'user_data' not in session:
            # OAuth2: Exchange the authorization code for an access token
            code = request.args.get('code')
            payload = {
                'client_id': SLACK_CLIENT_ID,
                'client_secret': SLACK_CLIENT_SECRET,
                'code': code
            }
            response = requests.post(SLACK_OAUTH_URL, data=payload)
            response_data = response.json()

            if 'access_token' not in response_data:
                redirect(url_for('index', redirect_url=request.url))

            # Fetch user information
            auth_token = response_data['access_token']
            user_id = response_data['authed_user']['id']
            headers = {'Authorization': f"Bearer {auth_token}"}
            user_response = requests.get(SLACK_USER_INFO_URL, headers=headers, params={'user': user_id})
            user_data = user_response.json()

            if user_data['ok']:
                session['access_token'] = auth_token
                session['user_data'] = user_data['user']
            else:
                redirect(url_for('index', redirect_url=request.url))

        if 'access_token' not in session or 'user_data' not in session:
            return redirect(url_for('index', redirect_url=request.url))
        return func(*args, **kwargs)

    wrapper.__name__ = func.__name__
    return wrapper


@app.route('/')
def index():
    redirect_path = request.args.get('redirect_path', 'forms')
    return render_template('sign-in.html', SLACK_CLIENT_ID=SLACK_CLIENT_ID, redirect_url=f'{DOMAIN}/{redirect_path}')


@app.route("/logout")
@user_logged_in
def logout():
    if "access_token" in session:
        session.pop("access_token")
    if "user_data" in session:
        session.pop("user_data")
    cookie_name = app.config.get("REMEMBER_COOKIE_NAME", SESSION_COOKIE_NAME)
    if cookie_name in request.cookies:
        session["_remember"] = "clear"
        if "_remember_seconds" in session:
            session.pop("_remember_seconds")
    return redirect('/')


@app.route("/slash-command", methods=['POST'])
@verify_slack_request
def slack_webhook():
    team_id = request.form['team_id']
    user_id = request.form['user_id']
    user_name = request.form['user_name']
    response_url = request.form['response_url']
    command_text = (request.form['text'] or '').replace("”", '"').replace("“", '"')
    args = shlex.split(command_text)
    result = None
    if len(args) < 1:
        result = slack_ui_blocks.help_text_block
    elif args[0] == "create":
        result = forms.create_form_command(team_id, user_id, user_name, args[1:], response_url)
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
        if action_id in (constants.FORM_WEEKDAYS, constants.FORM_TIME) or action.get('type') == 'static_select':
            return Response(status=200, mimetype="application/json")
        value = action['value']
        if action_id == constants.DELETE_FORM:
            result = forms.delete_form_command(value, user_id, response_url)
        elif action_id == constants.FILL_FORM_NOW:
            result = forms.fill_form_now_command(value, response_url)
        elif action_id == constants.SCHEDULE_FORM:
            result = schedules.schedule_form_command(value, response_url)
        elif action_id == constants.CREATE_FORM_SCHEDULE:
            schedule_form_state = payload['state']['values']
            result = schedules.create_form_schedule_command(value, user_id, user_name, schedule_form_state, response_url)
        elif action_id == constants.DELETE_SCHEDULE:
            result = schedules.delete_schedule_command(value, user_id, response_url)
        elif action_id == constants.SUBMIT_FORM_SCHEDULED:
            result = submissions.submit_scheduled_form(value, user_id, payload, response_url)
        elif action_id == constants.SUBMIT_FORM_NOW:
            result = submissions.submit_form_now(value, user_id, payload, response_url)
        elif action_id == constants.VIEW_FORM_SUBMISSIONS:
            result = submissions.view_submissions(value, user_id, response_url)
    if result:
        return Response(response=json.dumps(result), status=200, mimetype="application/json")
    return Response(status=200, mimetype="application/json")


@app.route('/forms', methods=['GET'])
@user_logged_in
def forms_view():
    forms = SlackForm.objects.filter(team_id=session['user_data']['team_id']).all()
    return render_template('forms.html', forms=forms, SLASH_COMMAND=SLASH_COMMAND)



@app.route('/submissions', methods=['GET'])
@user_logged_in
def get_submissions():
    form_id = request.args.get('formId')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))

    total = Submission.objects(form_id=form_id).count()
    submissions = Submission.objects(form_id=form_id).skip((page - 1) * per_page).limit(per_page)

    return render_template('submissions.html', submissions=submissions, page=page, per_page=per_page, total=total)
