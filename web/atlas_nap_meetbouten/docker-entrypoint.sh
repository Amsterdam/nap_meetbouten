#!/usr/bin/env bash

set -u
set -e

# collect static files
python manage.py collectstatic --noinput

# migrate database tables
yes yes | python manage.py migrate --noinput

# run uwsgi
uwsgi --ini /app/atlas_nap_meetbouten/uwsgi.ini
