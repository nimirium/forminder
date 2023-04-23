import logging
import os
from datetime import datetime, timedelta

from flask import Flask, request, render_template, session, redirect, make_response, send_from_directory, url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_session import Session
from pymongo import MongoClient

from src.constants import SLASH_COMMAND
from src.models.connect import connect_to_mongo
from src.models.form import SlackForm, Submission
from src.server_settings import MONGO_DB_URL, CustomRequest, SESSION_COOKIE_NAME, MONGO_DB_NAME
from views.view_utils import user_logged_in, form_visible_to_user
from views.views_v1 import urls_v1

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

connect_to_mongo()
pymongo_client = MongoClient(MONGO_DB_URL)

app = Flask(__name__, static_folder='ui/dist')
app.request_class = CustomRequest

app.config['SECRET_KEY'] = os.environ['SESSION_KEY']  # Replace with your secret key
app.config['SESSION_TYPE'] = 'mongodb'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_NAME'] = SESSION_COOKIE_NAME
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_MONGODB'] = pymongo_client
app.config['SESSION_MONGODB_DB'] = MONGO_DB_NAME

Session(app)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["60/minute"],
    storage_uri="memory://",
)


def user_is_logged_in():
    return 'access_token' in session and 'user_data' in session


# @app.route('/')
# def index():
#     if user_is_logged_in():
#         return redirect('/forms')
#     redirect_path = request.args.get('redirect_path', 'forms')
#     return render_template('sign-in.html', SLACK_CLIENT_ID=SLACK_CLIENT_ID, redirect_url=f'{DOMAIN}/{redirect_path}')


@app.route('/forms', methods=['GET'])
@user_logged_in
def forms_view():
    page = int(request.args.get('page', 1))
    per_page = min(int(request.args.get('per_page', 10)), 100)
    team_id = session['user_data']['team_id']
    total = SlackForm.objects(team_id=team_id).count()
    page_forms = SlackForm.objects(team_id=team_id).skip((page - 1) * per_page).limit(per_page)
    return render_template('forms.html', forms=page_forms, page=page, per_page=per_page,
                           total=total, SLASH_COMMAND=SLASH_COMMAND, navs=[dict(title='All Forms')])


@app.route('/submissions', methods=['GET'])
@user_logged_in
@form_visible_to_user
def submissions_view():
    # noinspection PyTypeHints
    request.slack_form: SlackForm
    form_id = str(request.slack_form.id)
    form = request.slack_form
    page = int(request.args.get('page', 1))
    per_page = min(int(request.args.get('per_page', 10)), 100)

    total = Submission.objects.filter(form_id=form_id).count()
    page_submissions = Submission.objects.filter(form_id=form_id).skip((page - 1) * per_page).limit(per_page)

    return render_template('submissions.html', form_id=form_id, submissions=page_submissions, page=page,
                           per_page=per_page, total=total, SLASH_COMMAND=SLASH_COMMAND,
                           navs=[dict(title='All Forms', path='/forms'), dict(title=form.name)])


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


_last_db_healthcheck = None


@app.route('/health')
def health_view():
    global _last_db_healthcheck
    if _last_db_healthcheck is None or _last_db_healthcheck < datetime.now() - timedelta(minutes=1):
        SlackForm.objects().first()  # check that the DB is not down
        _last_db_healthcheck = datetime.now()
    return make_response("OK", 200)


app.register_blueprint(urls_v1, url_prefix='/api/v1')


# Serve the frontend files
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    full_path = os.path.join(app.static_folder, path)
    if path and os.path.exists(full_path):
        return redirect(url_for('static', filename=path))
    else:
        return send_from_directory(app.static_folder, 'index.html')