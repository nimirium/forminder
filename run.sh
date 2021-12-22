# run mongo
mongod --config /usr/local/etc/mongod.conf --fork
# run server
export FLASK_APP=server
flask run

# see if mongo is runnung:
# ps aux | grep -v grep | grep mongod
