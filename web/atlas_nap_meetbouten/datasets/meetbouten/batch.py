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


class ImportMeetboutTask(batch.BasicTask):
    name = "Import MBT_MEETBOUT"
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
            rows = csv.reader(f, delimiter='|', quotechar='$', doublequote=True)
            meetbouten = [result for result in (self.process_row(row) for row in rows) if result]

        models.Meetbout.objects.bulk_create(meetbouten, batch_size=database.BATCH_SIZE)

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


class ImportReferentiepuntTask(batch.BasicTask):
    name = "Import MBT_REFERENTIEPUNT"
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
            rows = csv.reader(f, delimiter='|', quotechar='$', doublequote=True)
            referentiepunten = [result for result in (self.process_row(row) for row in rows) if result]

        models.Referentiepunt.objects.bulk_create(referentiepunten, batch_size=database.BATCH_SIZE)

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


class ImportMetingTask(batch.BasicTask):
    name = "Import MBT_METING"
    type_choices = dict()
    meetbouten = set()
    referentiepunten = set()
    referentiepunt_relations = list()

    def __init__(self, path):
        self.path = path

    def before(self):
        database.clear_models(models.Meting)
        self.type_choices = dict(models.Meting.TYPE_CHOICES)
        self.referentiepunten = frozenset(models.Referentiepunt.objects.values_list("pk", flat=True))
        self.meetbouten = frozenset(models.Meetbout.objects.values_list("pk", flat=True))

    def after(self):
        self.referentiepunten = None
        self.meetbouten = None

    def process(self):
        source = os.path.join(self.path, "MBT_METING.dat")
        with open(source, encoding='cp1252') as f:
            rows = csv.reader(f, delimiter='|', quotechar='$', doublequote=True)
            for row in rows:
                self.process_row(row)

            models.ReferentiepuntMeting.objects.bulk_create(self.referentiepunt_relations,
                                                            batch_size=database.BATCH_SIZE)

    def process_row(self, r):
        row = cleanup_row(r, replace=True)

        pk = row[0]
        meting_type = row[2]

        if meting_type not in self.type_choices:
            log.warn("Meting {} references non-existing type {}; skipping".format(pk, meting_type))
            return

        meetbout_id = row[5]
        if meetbout_id not in self.meetbouten:
            log.warn("Meting {} references non-existing meetbout {}; skipping".format(pk, meetbout_id))
            return

        meting = models.Meting.objects.create(
            pk=pk,
            datum=uva_datum(row[1]),
            type=meting_type,
            hoogte_nap=parse_decimal(row[3]),
            zakking=parse_decimal(row[4]),
            meetbout_id=meetbout_id,
            zakkingssnelheid=parse_decimal(row[9]),
            zakking_cumulatief=parse_decimal(row[10]),
            ploeg=row[11],
            type_int=int(row[12]) if row[12] else None,
            dagen_vorige_meting=int(row[13]) if row[13] else None,
            pandmsl=row[14],
            deelraad=row[15],
            wvi=row[16],
        )

        for i in range(6, 9):
            self.create_relation(meting, row[i])

        return meting

    def create_relation(self, meting, ref):
        if ref in self.referentiepunten:
            rm = models.ReferentiepuntMeting(
                referentiepunt_id=ref,
                meting=meting
            )
            self.referentiepunt_relations.append(rm)


class ImportRollaagTask(batch.BasicTask):
    name = "Import MBT_ROLLAAG"
    meetbouten = dict()

    def __init__(self, path):
        self.path = path

    def before(self):
        database.clear_models(models.Rollaag)
        self.meetbouten = {k: v for (k, v) in models.Meetbout.objects.values_list("bouwbloknummer", "pk")}

    def after(self):
        self.meetbouten.clear()

    def process(self):
        source = os.path.join(self.path, "MBT_ROLLAAG.dat")
        with open(source, encoding='cp1252') as f:
            rows = csv.reader(f, delimiter='|', quotechar='$', doublequote=True)
            rollagen = [result for result in (self.process_row(row) for row in rows) if result]

            models.Rollaag.objects.bulk_create(rollagen, batch_size=database.BATCH_SIZE)

    def process_row(self, r):
        row = cleanup_row(r, replace=True)

        pk = row[1]
        meetbout_id = self.meetbouten.get(row[0])

        if not meetbout_id:
            log.warn("Rollaag {} references non-existing meetbout {}; skipping".format(pk, row[0]))
            return

        return models.Rollaag(
            pk=pk,
            meetbout_id=meetbout_id,
            locatie_x=parse_decimal(row[2]),
            locatie_y=parse_decimal(row[3]),
            geometrie=GEOSGeometry(row[4]),
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
            ImportMeetboutTask(self.meetbouten),
            ImportReferentiepuntTask(self.meetbouten),
            ImportMetingTask(self.meetbouten),
            ImportRollaagTask(self.meetbouten),
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
