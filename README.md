# slack-askme-reminders

Schedule slack to remind you to fill a daily form



## Installation - run locally

### install virtual environment and run
```
virtualenv -p `which python3.8` .venv
source /.venv/bin/activate
pip install -r requirements.txt
export FLASK_APP=server
flask server
```

### run locally with ngrok
for a quick dev https address, run locally with ngrok: 

`ngrok http 5000`

You'll get an https address like `https://XXXXXXXXXXXXXXX.ngrok.io`. 
Use it instead of YOUR_DOMAIN in the next step.

### configure slack app
1. Create a slack command which points `/ask-remind` to `YOUR_DOMAIN/slack-webhook`
2. Set interactivity request url to `YOUR_DOMAIN/slack-interactive-endpoint`
3. Create a bot user OAuth token in slack, and put it in an `.env` file
```shell
SLACK_BOT_TOKEN=xoxb-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

