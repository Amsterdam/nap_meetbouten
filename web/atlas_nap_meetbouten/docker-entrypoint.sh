#!/usr/bin/env bash

set -u   # crash on missing env variables
set -e   # stop on any error

cd /app

# collect static files
python manage.py collectstatic --noinput

# migrate database tables
yes yes | python manage.py migrate --noinput

# run uwsgi
exec uwsgi --ini /app/uwsgi.ini
