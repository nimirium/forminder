from flask import Flask, request

app = Flask(__name__)


@app.route("/slack-webhook", methods=['POST'])
def slack_webhook():
    print(f"request.form: {request.form}")
    token = request.form['token']
    team_id = request.form['team_id']
    team_domain = request.form['team_domain']
    channel_id = request.form['channel_id']
    channel_name = request.form['channel_name']
    user_id = request.form['user_id']
    user_name = request.form['user_name']
    command = request.form['command']
    text = request.form['text']
    api_app_id = request.form['api_app_id']
    is_enterprise_install = request.form['is_enterprise_install']
    response_url = request.form['response_url']
    trigger_id = request.form['trigger_id']
    return "<p>Hello, World!</p>"
