import json
import shlex

from flask import Flask, request, Response

from controllers import forms, schedules
from util import slack_blocks
from models.connect import connect_to_mongo

app = Flask(__name__)
connect_to_mongo()

DAYS_OF_THE_WEEK = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]


@app.route("/slack-webhook", methods=['POST'])
def slack_webhook():
    print(f"request.form: {request.form}")
    user_id = request.form['user_id']
    user_name = request.form['user_name']
    response_url = request.form['response_url']
    command_text = (request.form['text'] or '').replace("”", '"').replace("“", '"')
    args = shlex.split(command_text)
    result = None
    if len(args) == 0:
        result = slack_blocks.help_text_block
    elif args[0] == "create-form":
        result = forms.create_form_command(user_id, user_name, args, response_url)
    elif args[0] == "schedule":
        result = schedules.handle_schedule_command()
    elif args[0] == "list":
        if len(args) < 2:
            result = slack_blocks.help_text_block
        elif args[1] == "forms":
            result = forms.list_forms_command(user_id, response_url)
        elif args[1] == "schedules":
            result = schedules.list_schedules()
    print(f"result is {result}")
    if result:
        return Response(response=json.dumps(result), status=200, mimetype="application/json")
    return Response(status=200, mimetype="application/json")


@app.route("/slack-interactive-endpoint", methods=['POST'])
def slack_interactive_endpoint():
    print(f"request.form: {request.form}")
    return Response(status=200)
