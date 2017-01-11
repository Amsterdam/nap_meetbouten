#!/usr/bin/env bash

set -u   # crash on missing env variables
set -e   # stop on any error

exec python manage.py test
