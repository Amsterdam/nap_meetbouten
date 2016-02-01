import logging
import os
import csv

from django.conf import settings
from django.contrib.gis.geos import GEOSGeometry

from datapunt_generic.batch import batch
from datapunt_generic.generic import database, index

from datapunt_generic.generic.csv import cleanup_row, parse_decimal
from datapunt_generic.generic.uva2 import uva_indicatie, uva_datum
from . import models, documents

log = logging.getLogger(__name__)


class ImportMeetboutenTask(batch.BasicTask):
    name = "Import Meetbouten"
    meetbouten = dict()
    status_choices = dict()

    def __init__(self, path):
        self.path = path

    def before(self):
        self.status_choices = dict(models.Meetbout.STATUS_CHOICES)
        database.clear_models(models.Meetbout)

    def after(self):
        pass

    def process(self):
        source = os.path.join(self.path, "MBT_MEETBOUT.dat")
        with open(source, encoding='cp1252') as f:
            rows = csv.reader(
                f, delimiter='|', quotechar='$', doublequote=True)
            self.meetbouten = [
                result for result in (
                    self.process_row(row)
                    for row in rows) if result]

        models.Meetbout.objects.bulk_create(
            self.meetbouten, batch_size=database.BATCH_SIZE)

    def process_row(self, r):
        row = cleanup_row(r, replace=True)

        pk = row[0]
        status = row[14]

        if status not in self.status_choices:
            log.warn("Meetbout {} references non-existing status {}; skipping".format(pk, status))
            return

        return models.Meetbout(
            pk=pk,
            buurt=row[1],
            locatie_x=parse_decimal(row[2]),
            locatie_y=parse_decimal(row[3]),
            hoogte_nap=parse_decimal(row[4]),
            zakking_cumulatief=parse_decimal(row[5]),
            datum=uva_datum(row[6]),
            bouwblokzijde=row[7],
            eigenaar=row[8],
            beveiligd=uva_indicatie(row[9]),
            deelraad=row[10],
            nabij_adres=row[11],
            locatie=row[12],
            zakkingssnelheid=parse_decimal(row[13]),
            status=status,
            bouwbloknummer=row[15],
            blokeenheid=row[16] or 0,
            geometrie=GEOSGeometry(row[17]),
        )


class ImportReferentiepuntenTask(batch.BasicTask):
    name = "Import Referentiepunten"
    referentiepunten = dict()

    def __init__(self, path):
        self.path = path

    def before(self):
        database.clear_models(models.Referentiepunt)

    def after(self):
        pass

    def process(self):
        source = os.path.join(self.path, "MBT_REFERENTIEPUNT.dat")
        with open(source, encoding='cp1252') as f:
            rows = csv.reader(
                f, delimiter='|', quotechar='$', doublequote=True)
            self.referentiepunten = [
                result for result in (
                    self.process_row(row) for row in rows) if result]

        models.Referentiepunt.objects.bulk_create(
            self.referentiepunten, batch_size=database.BATCH_SIZE)

    def process_row(self, r):
        row = cleanup_row(r, replace=True)

        pk = row[0]

        return models.Referentiepunt(
            pk=pk,
            locatie_x=parse_decimal(row[1]),
            locatie_y=parse_decimal(row[2]),
            hoogte_nap=parse_decimal(row[3]),
            datum=uva_datum(row[4]),
            locatie=row[5],
            geometrie=GEOSGeometry(row[6]),
        )


class ImportMeetboutenJob(object):
    name = "Import meetbouten"

    def __init__(self):
        diva = settings.DIVA_DIR
        if not os.path.exists(diva):
            raise ValueError("DIVA_DIR not found: {}".format(diva))

        self.meetbouten = os.path.join(diva, 'meetbouten')

    def tasks(self):
        return [
            ImportMeetboutenTask(self.meetbouten),
            ImportReferentiepuntenTask(self.meetbouten),
        ]


#
# Elastic jobs
#


class IndexMeetboutenTask(index.ImportIndexTask):
    name = "index meetbouten aanduidingen"

    queryset = models.Meetbout.objects

    def convert(self, obj):
        return documents.from_meetbout(obj)


class DeleteMeetboutenIndexTask(index.DeleteIndexTask):
    index = settings.ELASTIC_INDICES['MEETBOUTEN']
    doc_types = [documents.Meetbout]


class DeleteMeetboutenBackupIndexTask(index.DeleteIndexTask):
    index = settings.ELASTIC_INDICES['MEETBOUTEN']
    doc_types = [documents.Meetbout]


class BackupMeetboutenIndexTask(index.CopyIndexTask):
    """
    Backup elastic Meetbouten Index
    """
    name = 'Backup meetbouten index in elastic'

    index = settings.ELASTIC_INDICES['MEETBOUTEN']
    target = settings.ELASTIC_INDICES['MEETBOUTEN'] + 'backup'


class RestoreMeetboutenIndexTask(index.CopyIndexTask):
    """
    Restore elastic BAG Index
    """
    name = 'Restore backup meetbouten index in elastic'

    index = settings.ELASTIC_INDICES['MEETBOUTEN'] + 'backup'
    target = settings.ELASTIC_INDICES['MEETBOUTEN']


class IndexMeetboutenJob(object):
    name = "Create new search-index for meetbouten data in database"

    def tasks(self):
        return [
            DeleteMeetboutenIndexTask(),
            IndexMeetboutenTask()
        ]


class BackupMeetboutenJob(object):
    """
    Backup elastic BAG documents
    """
    name = "Backup elastic-index Meetbouten"

    def tasks(self):
        return [
            DeleteMeetboutenBackupIndexTask,
            BackupMeetboutenIndexTask(),
        ]


class RestoreMeetboutenJob(object):

    name = "Restore Backup elastic-index Meetbouten"

    def tasks(self):
        return [
            DeleteMeetboutenIndexTask(),
            RestoreMeetboutenIndexTask()
        ]
