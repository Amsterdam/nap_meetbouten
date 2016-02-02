import re
import os
import subprocess

from django.db import connection

BATCH_SIZE = 50000


def clear_models(*models):
    """
    Truncates the table associated with ``model`` and all related tables.
    """
    for model in models:
        # noinspection PyProtectedMember
        connection.cursor().execute("TRUNCATE {} CASCADE".format(model._meta.db_table))


def get_docker_host(host='database'):
    """
    if any container name matches 'host' name the ip is returned
    else returns 'localhost'
    """
    d_host = None
    output = subprocess.check_output(['docker', 'ps'], universal_newlines=True)
    container_lines = output.split('\n')[1:-1]
    container_names = [line.split()[-1] for line in container_lines]

    print('Dockers containers: \n %s' % ', '.join(container_names))

    def get_ip(name):
        ip_data = subprocess.check_output([
            'docker', 'inspect',
            '--format', "'{{ .NetworkSettings.IPAddress }}'", name],
            universal_newlines=True
            )

        ip_data = ip_data.replace("'", '')
        ip_data = ip_data.replace('\n', '')

        return ip_data

    for name in container_names:
        if host in name:
            d_host = get_ip(name)

    if d_host:
        if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', d_host):
            return d_host

        return re.match(r'tcp://(.*?):\d+', d_host).group(1)

    return 'localhost'
