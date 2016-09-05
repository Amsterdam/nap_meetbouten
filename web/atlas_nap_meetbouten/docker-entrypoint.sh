#!/usr/bin/env bash

set -u   # crash on missing env variables
set -e   # stop on any error

cd /app

source docker-wait.sh

# migrate database tables
yes yes | python manage.py migrate --noinput

# create geotables and indices
python manage.py create_geo_tables

# run uwsgi
exec uwsgi --ini /app/uwsgi.ini

