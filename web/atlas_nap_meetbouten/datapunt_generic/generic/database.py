import re
import os
from django.db import connection

BATCH_SIZE = 50000


def clear_models(*models):
    """
    Truncates the table associated with ``model`` and all related tables.
    """
    for model in models:
        # noinspection PyProtectedMember
        connection.cursor().execute("TRUNCATE {} CASCADE".format(model._meta.db_table))


def get_docker_host():
    # TODO:
    """
    integrate this (postactivate virtualenv) bash code here?

    DB_DOCKER_NAME='kartoza/postgis'
    CONTAINER=$(docker ps | grep $DB_DOCKER_NAME | awk '{ print $1 }')
    DOCKER_HOST=$(docker inspect $CONTAINER | grep IPAddress | awk '{ print $2 }' | tr -d ',"' | tr -d 'null')

    export
    """
    d_host = os.getenv('DOCKER_HOST', None)
    if d_host:
        if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', d_host):
            return d_host

        return re.match(r'tcp://(.*?):\d+', d_host).group(1)
    return 'localhost'
