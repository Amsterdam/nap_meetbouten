Atlas NAP & Meetbouten
======================


Requirements
------------

* Docker-Compose (required)


Developing
----------

Use `docker-compose` to start a local database.

	(sudo) docker-compose start -d

or

	docker-compose up -d

The API should now be available on http://localhost:8100/nap

To run an import, execute:

	./nap_meetbouten/manage.py run_import


To see the various options for partial imports, execute:

	./nap_meetbouten/manage.py run_import --help


To import the latest database from acceptance:

	docker-compose exec -it nap_meetbouten_database_1 update-nap.sh

To import the latest elastic index from acceptance:

	docker-compose exec -it nap_meetbouten_elasticsearch_1 update-meetbouten.sh

