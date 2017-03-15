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
import zipfile

from functools import lru_cache
from dateutil import parser
from pathlib import Path

from swiftclient.client import Connection

log = logging.getLogger(__name__)

logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("swiftclient").setLevel(logging.WARNING)

assert os.getenv('BAG_OBJECTSTORE_PASSWORD')

os_connect = {
    'auth_version': '2.0',
    'authurl': 'https://identity.stack.cloudvps.com/v2.0',
    'user': 'bag_brk',
    'key': os.getenv('BAG_OBJECTSTORE_PASSWORD', 'insecure'),
    'tenant_name': 'BGE000081_BAG',
    'os_options': {
        'tenant_id': '4f2f4b6342444c84b3580584587cfd18',
        'region_name': 'NL',
        # 'endpoint_type': 'internalURL'
    }
}

DIVA_DIR = '/app/data'


@lru_cache(maxsize=None)
def get_conn():
    assert os.getenv('BAG_OBJECTSTORE_PASSWORD')
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


def download_diva_file(container_name, file_path, target_path=None):
    """
    Download a diva file
    :param container_name:
    :param mapped_folder: the foldername where file is written to
    :param folder: foldername in O/S
    :param file_name:
    :return:
    """

    path = file_path.split('/')

    file_name = path[-1]
    log.info("Create file {} in {}".format(DIVA_DIR, file_name))
    file_name = path[-1]

    if target_path:
        newfilename = '{}/{}'.format(DIVA_DIR, target_path)
    else:
        newfilename = '{}/{}'.format(DIVA_DIR, file_name)

    if file_exists(newfilename):
        log.debug('Skipped file exists: %s', newfilename)
        return

    with open(newfilename, 'wb') as newfile:
        zipdata = get_conn().get_object(container_name, file_path)[1]
        newfile.write(zipdata)


def download_zips(container_name, zips_mapper):
    """
    Download latest zips
    """

    for _, zipfiles in zips_mapper.items():
        zipfiles.sort(reverse=True)
        zip_name = zipfiles[0][1]['name']
        download_diva_file(container_name, zip_name)


zip_age_limits = {
  'NAP.zip': 14,
}


def check_age(zip_created, file_key, file_object):
    """
    Do basic sanity check on zip delivery..
    """

    now = datetime.datetime.today()
    delta = now - zip_created
    log.debug('AGE: %2d days', delta.days)
    source_name = file_object['name']

    log.debug('%s_%s' % (zip_created.strftime('%Y%m%d'), file_key))

    for key, agelimit in zip_age_limits.items():
        if file_key.endswith(key):
            if zip_age_limits[key] < delta.days:
                raise ValueError(
                    f"""

        Zip delivery is late!

        {key} age: {delta.days}  max_age: {zip_age_limits[key]}

        from {source_name}

                    """)


def validate_age(zips_mapper):
    """
    Check if the files we want to import are not to old!
    """
    log.debug('validating age..')

    for zipkey, zipfiles in zips_mapper.items():

        # this is the file we want to import
        age, importsource = zipfiles[0]

        check_age(age, zipkey, importsource)

        log.debug('OK: %s %s', age, zipkey)


def create_target_directories():
    """
    the directories where the import proces expects the import source files
    should be created before unzipping files.
    """

    # Make sure target directories exist
    for target in path_mapping.values():
        directory = os.path.join(DIVA_DIR, target)
        if not os.path.exists(directory):
            os.makedirs(directory)


path_mapping = {
    'MBT': 'meetbouten',
    'NAP': 'nap',
}


def unzip_files(zipsource):
    """
    Unzip single files to the right target directory
    """

    # Extract files to the expected location
    directory = os.path.join(DIVA_DIR)

    for fullname in zipsource.namelist():
        zipsource.extract(fullname, directory)
        file_name = fullname.split('/')[-1]
        for path, target in path_mapping.items():
            if path in fullname:
                source = f"{directory}/{fullname}"
                target = f'{directory}/{target}/{file_name}'
                # relocate fiel to expected location
                print(source)
                print(target)
                os.rename(source, target)


def unzip_data(zips_mapper):
    """
    unzip the zips
    """

    for zipkey, zipfiles in zips_mapper.items():

        latestzip = zipfiles[0][1]

        filepath = latestzip['name'].split('/')
        file_name = filepath[-1]
        zip_path = '{}/{}'.format(DIVA_DIR, file_name)

        log.info("Unzip {}".format(zip_path))

        zipsource = zipfile.ZipFile(zip_path, 'r')
        unzip_files(zipsource)


def delete_from_objectstore(container, object_name):
    """
    remove file `object_name` fronm `container`
    :param container: Container name
    :param object_name:
    :return:
    """
    return get_conn().delete_object(container, object_name)


def delete_old_zips(container_name, zips_mapper):
    """
    Cleanup old zips
    """
    for zipkey, zipfiles in zips_mapper.items():
        log.debug('KEEP : %s', zipfiles[0][1]['name'])
        if len(zipfiles) > 1:
            # delete old files
            for _, zipobject in zipfiles[1:]:
                zippath = zipobject['name']
                log.debug('PURGE: %s', zippath)
                delete_from_objectstore(container_name, zippath)


def fetch_diva_zips(container_name, zipfolder):
    """
    fetch files from folder in an objectstore container
    :param container_name:
    :param folder:
    :return:
    """
    log.info("import files from {}".format(zipfolder))

    zips_mapper = {}

    for file_object in get_full_container_list(
            container_name, prefix=zipfolder):

        if file_object['content_type'] == 'application/directory':
            continue

        path = file_object['name'].split('/')
        file_name = path[-1]

        if not file_name.endswith('.zip'):
            continue

        if not any(pattern in file_name for pattern in ['NAP', 'MBT']):
            continue

        dt = parser.parse(file_object['last_modified'])

        file_key = "".join(file_name.split('_')[1:])

        zips_mapper.setdefault(file_key, []).append((dt, file_object))

    download_zips(container_name, zips_mapper)
    delete_old_zips(container_name, zips_mapper)

    validate_age(zips_mapper)

    unzip_data(zips_mapper)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    # Download files from objectstore
    log.info("Start downloading files from objectstore")
    create_target_directories()
    fetch_diva_zips('Diva', 'Zip_bestanden')
    log.info("Finished downloading files from objectstore")
