# slack-forminder

Effortlessly manage form-filling on Slack. Create customized forms, schedule reminders, and streamline your workflow with ease.

## Installation - run locally

### Run MongoDB
install mongodb guide: https://www.mongodb.com/docs/manual/installation/

on mac, start mongodb with: `brew services start mongodb-community@6.0`

### install virtual environment and run
```
virtualenv -p `which python3` .venv
source .venv/bin/activate
pip install -r requirements.txt
export FLASK_APP=server
flask run
```

### run locally with ngrok
for a quick dev https address, run locally with ngrok: 

`ngrok http 5000`

You'll get an https address like `https://XXXXXXXXXXXXXXX.ngrok.io`. 
Use it instead of YOUR_DOMAIN in the next step.

### configure slack app
1. Create a slash command which points `/forminder` to `YOUR_DOMAIN/slash-command`
2. In "Interactivity & Shortcuts", set interactivity request url to `YOUR_DOMAIN/interactive`
3. Create a bot user OAuth token in slack, and put it in an `.env` file
4. Add your signing secret (from the Basic Information tab) to the `.env` file
5. Add OAuth redirect urla that point to `YOUR_DOMAIN/forms` and `YOUR_DOMAIN/submissions`
```shell
SLACK_BOT_TOKEN=xoxb-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
SIGNING_SECRET=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

### Run the scheduler
```python scheduling_worker.py```
