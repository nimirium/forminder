import logging
import os

from mongoengine import connect


def connect_to_mongo():
    db_url = os.environ['MONGO_DB_URL']
    try:
        logging.info(f"connecting to mongo db: mongodb://mongo:********@{db_url.split('@')[1]}")
    except IndexError:
        logging.info(f"connecting to local mongo db")
    connect(host=db_url)
