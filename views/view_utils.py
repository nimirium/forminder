import json
import os

import bson
import requests
from flask import request, Response, session, redirect, url_for, make_response, send_from_directory
from jinja2 import Environment, FileSystemLoader
from slack_sdk.signature import SignatureVerifier

from src.models.form import SlackForm
from src.server_settings import SLACK_CLIENT_ID, SLACK_CLIENT_SECRET, SLACK_OAUTH_URL, SLACK_USER_INFO_URL
from src.slack_api.slack_user import SlackUser

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
                return redirect(url_for('catch_all', path='login'))

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
                return redirect(url_for('catch_all', path='login'))

        if 'access_token' not in session or 'user_data' not in session:
            return redirect(url_for('catch_all', path='login'))
        request.user = SlackUser(user_id=session['user_data']['id'])
        return func(*args, **kwargs)

    wrapper.__name__ = func.__name__
    return wrapper


def form_visible_to_user(func, *args, **kwargs):
    def wrapper():
        form_id = request.args.get('formId')
        if not form_id:
            return make_response("You must provide formId query parameter", 400)
        try:
            form = SlackForm.objects.filter(id=form_id).first()
        except bson.errors.InvalidId:
            return make_response("Form not found", 404)
        # noinspection PyUnresolvedReferences
        if form.team_id != request.user.team_id:
            # noinspection PyUnresolvedReferences
            logging.warning(f"User {request.user.id} tried to access a form that doesn't belong to their team")
            return make_response("Form not found", 404)
        request.slack_form = form
        return func(*args, **kwargs)

    wrapper.__name__ = func.__name__
    return wrapper


def serve_ui(path: str):
    if path and os.path.exists('ui/dist/' + path):
        return send_from_directory('ui/dist', path)
    else:
        if hasattr(request, 'user') and request.user:
            user = request.user.to_dict()
            response = make_response(send_from_directory('ui/dist', 'index.html'))
            response.headers['X-User'] = json.dumps(user)
            return response
        return send_from_directory('ui/dist', 'index.html')
