import os

import requests
from flask import jsonify, request, session, redirect, url_for
import functools

from src.server_settings import SLACK_CLIENT_ID, SLACK_CLIENT_SECRET, SLACK_OAUTH_URL, SLACK_USER_INFO_URL
from src.slack_api.slack_user import SlackUser


def slack_auth() -> bool:
    """
    Checks if the user is logged in with slack
    :return: Bool - whether the user is logged in
    """
    if request.args.get('code') and ('access_token' not in session or 'user_data' not in session):
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
            return False

        # Fetch user information
        auth_token = response_data['access_token']
        user_id = response_data['authed_user']['id']
        headers = {
            'Authorization': f"Bearer {auth_token}"
        }
        user_response = requests.get(SLACK_USER_INFO_URL, headers=headers, params={
            'user': user_id
        })
        user_data = user_response.json()

        if user_data['ok']:
            session['access_token'] = auth_token
            session['user_data'] = user_data['user']
        else:
            return False

    if 'access_token' not in session or 'user_data' not in session:
        return False

    request.user = SlackUser(user_id=session['user_data']['id'])
    return True


def user_logged_in_ui(func):
    """ Decorator - make sure user is logged in, if not, redirect to /login """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not slack_auth():
            return redirect(url_for('catch_all', path='login'))
        return func(*args, **kwargs)

    return wrapper


def setup_for_debug():
    """ This is needed to run locally without HTTPS """
    session['team_id'] = os.environ['DEV_TEAM_ID']
    session['user_data'] = {
        'id': os.environ['DEV_USER_ID'],
        'team_id': os.environ['DEV_TEAM_ID'],
    }
    request.user = SlackUser(user_id=session['user_data']['id'])


def user_logged_in_api(func):
    """ Decorator - make sure user is logged in, if not, return 401 """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if os.environ.get('FLASK_DEBUG'):
            setup_for_debug()
        elif not slack_auth():
            return jsonify({"error": "Unauthorized"}), 401
        return func(*args, **kwargs)

    return wrapper
