# run mongo
mongod --config /usr/local/etc/mongod.conf --fork
# run server
export FLASK_APP=server
export MONGO_DB_NAME=dev
python scheduling_worker.py >> scheduling_worker.log 2>&1 &
flask run

# see if mongo is runnung:
# ps aux | grep -v grep | grep mongod
