#!/usr/bin/env bash

set -u
set -e

cd /app

# wait for elastic
while ! nc -z ${ELASTIC_PORT_9200_TCP_ADDR} ${ELASTIC_PORT_9200_TCP_PORT}
do
	echo "Waiting for elastic..."
	sleep 0.1
done

# wait for postgres
while ! nc -z ${DATABASE_PORT_5432_TCP_ADDR} ${DATABASE_PORT_5432_TCP_PORT}
do
	echo "Waiting for postgres..."
	sleep 0.1
done

# collect static files
python manage.py collectstatic --noinput

# migrate database tables
yes yes | python manage.py migrate --noinput

# run uwsgi
exec uwsgi --ini /app/uwsgi.ini
