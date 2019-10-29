"""
Module Contains logic to get the latest most up to date
files to import in the NAP database

Goal is to assure we load Datapunt with accurate and current data

checks:

   check AGE of filenames
     - we do not work with old data
   check filename changes
     - we do not work of old files because new files are renamed

We download specific zip files:

Unzip target data in to empty new location and start
import proces.


"""

import logging
import os
import datetime

from functools import lru_cache
from dateutil import parser
from pathlib import Path

from swiftclient.client import Connection

log = logging.getLogger(__name__)

logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("swiftclient").setLevel(logging.WARNING)

DIVA_DIR = '/app/data'

environment = os.getenv('GOB_OBJECTSTORE_ENV', 'productie')
os_connect = {
    'auth_version': '2.0',
    'authurl': 'https://identity.stack.cloudvps.com/v2.0',
    'user': 'GOB_user',
    'key': os.getenv('GOB_OBJECTSTORE_PASSWORD', 'insecure'),
    'tenant_name': 'BGE000081_GOB',
    'os_options': {
        'tenant_id': '2ede4a78773e453db73f52500ef748e5',
        'region_name': 'NL',
    }
}


@lru_cache(maxsize=None)
def get_conn():
    assert os.getenv('GOB_OBJECTSTORE_PASSWORD')
    return Connection(**os_connect)


def file_exists(target):
    target = Path(target)
    return target.is_file()


def get_full_container_list(container_name, **kwargs):
    """
    Return a listing of filenames in container `container_name`
    :param container_name:
    :param kwargs:
    :return:
    """
    limit = 10000
    kwargs['limit'] = limit
    page = []
    seed = []
    _, page = get_conn().get_container(container_name, **kwargs)
    seed.extend(page)

    while len(page) == limit:
        # keep getting pages..
        kwargs['marker'] = seed[-1]['name']
        _, page = get_conn().get_container(container_name, **kwargs)
        seed.extend(page)

    return seed


def download_file(container_name, file_path, target_path=None, file_last_modified=None):
    path = file_path.split('/')

    file_name = path[-1]
    log.info(f"Create file {file_name} in {DIVA_DIR}")

    if target_path:
        newfilename = '{}/{}'.format(DIVA_DIR, target_path)
    else:
        newfilename = '{}/{}'.format(DIVA_DIR, file_name)

    if file_exists(newfilename):
        log.debug('Skipped file exists: %s', newfilename)
        return

    with open(newfilename, 'wb') as newfile:
        data = get_conn().get_object(container_name, file_path)[1]
        newfile.write(data)
    if file_last_modified:
        epoch_modified = file_last_modified.timestamp()
        os.utime(newfilename, (epoch_modified, epoch_modified))


gob_file_age_and_target_list = {
    'meetbouten/DAT/MBT_MEETBOUT.dat': (30, 'meetbouten/MBT_MEETBOUT.dat'),
    'meetbouten/DAT/MBT_METING.dat': (30, 'meetbouten/MBT_METING.dat'),
    'meetbouten/DAT/MBT_REFERENTIEPUNT.dat': (30, 'meetbouten/MBT_REFERENTIEPUNT.dat'),
    'meetbouten/DAT/MBT_ROLLAAG.dat': (30, 'meetbouten/MBT_ROLLAAG.dat'),
    'nap/DAT/NAP_PEILMERK.dat': (30, 'nap/NAP_PEILMERK.dat'),
}


def fetch_gob_files(container_name, prefix):
    logging.basicConfig(level=logging.DEBUG)
    now = datetime.datetime.today()

    for file_object in get_full_container_list(container_name, prefix=prefix):

        if file_object['content_type'] == 'application/directory':
            continue

        file_path = file_object['name']
        path = file_path.split('/')

        file_max_age_and_target = gob_file_age_and_target_list.get(file_path)
        file_name = path[-1]

        if not file_max_age_and_target:
            continue

        (file_max_age, file_target) = file_max_age_and_target
        file_last_modified = parser.parse(file_object['last_modified'])

        delta = now - file_last_modified
        log.debug('AGE %s: %2d days', file_name, delta.days)

        if delta.days > file_max_age:
            raise ValueError(f"""

            Delivery of file {file_name }is late!

            {file_path} age {delta.days} max_age: {file_max_age}
            """)

        directory = os.path.join(DIVA_DIR, *path[:-1])
        if not os.path.exists(directory):
            os.makedirs(directory)

        download_file(container_name, file_path, target_path=file_target,
                      file_last_modified=file_last_modified)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    # Download files from objectstore
    log.info("Start downloading files from objectstore")
    fetch_gob_files(environment, 'meetbouten')
    fetch_gob_files(environment, 'nap')
    log.info("Finished downloading files from objectstore")
