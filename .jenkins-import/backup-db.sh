#!/usr/bin/env bash

set -u
set -e
set -x

echo 0.0.0.0:5432:nap:nap:insecure > ~/.pgpass
chmod 600 ~/.pgpass

pg_dump -Fc -h 0.0.0.0 -U nap nap > /tmp/backups/database.dump
