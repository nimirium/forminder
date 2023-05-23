import json
import os

import bson
from flask import request, Response, make_response, send_from_directory
from slack_sdk.signature import SignatureVerifier

from src.models.form import SlackForm

slack_verifier = SignatureVerifier(os.environ['SIGNING_SECRET'])


def verify_slack_request(func, *args, **kwargs):
    """ Decorator for endpoints that handle requests from slack """
    def wrapper():
        if slack_verifier.is_valid_request(request.get_data(), request.headers):
            return func(*args, **kwargs)
        return Response(status=401)

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
    """ Serve Vue.js website """
    if path and os.path.exists('ui/dist/' + path):
        return send_from_directory('ui/dist', path)
    return send_from_directory('ui/dist', 'index.html')
