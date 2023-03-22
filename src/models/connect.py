import logging
import os

from mongoengine import connect


def connect_to_mongo():
    dbname = os.environ['MONGO_DB_NAME']
    logging.info(f"connecting to mongo db: {dbname}")
    connect('test')
