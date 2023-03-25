import logging
import os

from mongoengine import connect


def connect_to_mongo():
    db_url = os.environ['MONGO_DB_URL']
    logging.info(f"connecting to mongo db: mongodb://mongo:********@{db_url.split('@')[1]}")
    connect(host=db_url)
