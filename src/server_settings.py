import os
from typing import Optional

from flask import Request as FlaskRequest

SLACK_CLIENT_ID = os.environ["SLACK_CLIENT_ID"]
SLACK_CLIENT_SECRET = os.environ["SLACK_CLIENT_SECRET"]
SLACK_OAUTH_URL = "https://slack.com/api/oauth.v2.access"
SLACK_USER_INFO_URL = "https://slack.com/api/users.info"
DOMAIN = os.environ['DOMAIN']
MONGO_DB_URL = os.environ['MONGO_DB_URL']
MONGO_DB_NAME = os.environ['MONGO_DB_NAME']
SESSION_COOKIE_NAME = 'session'


class CustomRequest(FlaskRequest):
    """ Override Flask request class. Helps with typing """
    user: Optional['SlackUser']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
