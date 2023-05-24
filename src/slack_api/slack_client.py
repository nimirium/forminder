import os

import cachetools as cachetools
from flask import session
from slack_sdk import WebClient

# Cache with a max size of 100 and a 2-minute (120 seconds) expiration time
_users_cache = cachetools.TTLCache(maxsize=1000, ttl=120)
_slack_client = None


def get_slack_client():
    global _slack_client
    if _slack_client is None:
        _slack_client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))
    return _slack_client


def get_users_info(user_id):
    """ Calls slack API to get user info, and saves it in a local cache. """
    if user_id not in _users_cache:
        client = get_slack_client()
        client.token = session['access_token']
        users_info = client.users_info(user=user_id)
        user_data = users_info.data['user']
        _users_cache[user_id] = {
            'is_admin': user_data['is_admin'],
            'tz': user_data['tz'],
            'username': user_data['name'],
            'team_id': user_data['team_id'],
        }
    return _users_cache[user_id]
