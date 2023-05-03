.PHONY: all release run-mongo run-worker build-ui setup-server run-server build-dev-ui build-release-ui clean

all: run-worker build-dev-ui run-server
release: build-release-ui

run-mongo:
	mongod --config /usr/local/etc/mongod.conf --fork

run-worker:
	python scheduling_worker.py >> scheduling_worker.log 2>&1 &

setup-server:
	export FLASK_APP=server
	export MONGO_DB_NAME=dev

run-server: setup-server
	flask --app server run

build-ui:
	cd ui && npm run build && cd ..

build-dev-ui:
	cp ui/.env_dev ui/.env
	$(MAKE) build-ui

build-release-ui:
	cp ui/.env_prod ui/.env
	$(MAKE) build-ui

clean:
	killall mongod
	killall python
