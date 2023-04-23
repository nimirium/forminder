import logging
import os
from datetime import datetime, timedelta

from flask import Flask, request, session, redirect, make_response, send_from_directory
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_session import Session
from pymongo import MongoClient

from src.models.connect import connect_to_mongo
from src.models.form import SlackForm
from src.server_settings import MONGO_DB_URL, CustomRequest, SESSION_COOKIE_NAME, MONGO_DB_NAME
from views.view_utils import user_logged_in, serve_ui
from views.views_v1 import urls_v1

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

connect_to_mongo()
pymongo_client = MongoClient(MONGO_DB_URL)

app = Flask(__name__)
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


@app.route('/forms', methods=['GET'])
@user_logged_in
def forms_ui():
    return serve_ui('forms')


@app.route('/submissions', methods=['GET'])
@user_logged_in
def submissions_ui():
    return serve_ui('submissions')


# Serve the frontend files
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return serve_ui(path)
