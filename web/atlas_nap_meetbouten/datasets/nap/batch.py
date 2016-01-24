import logging
import os
import csv

from django.conf import settings
from django.contrib.gis.geos import GEOSGeometry

from datapunt_generic.batch import batch
from datapunt_generic.generic import database

from .models import Peilmerk

log = logging.getLogger(__name__)


class ImportNapTask(batch.BasicTask):
    name = "Import NAP"
    peilmerken = dict()

    def __init__(self, path):
        self.path = path

    def before(self):
        database.clear_models(Peilmerk)

    def after(self):
        pass

    def process(self):
        source = os.path.join(self.path, "NAP_PEILMERK.dat")
        with open(source, encoding='cp1252') as f:
            rows = csv.reader(f, delimiter='|', quotechar='$')
            self.peilmerken = [result for result in (self.process_row(row) for row in rows) if result]

        Peilmerk.objects.bulk_create(self.peilmerken, batch_size=database.BATCH_SIZE)

    def process_row(self, r):
        row = list()
        for i in range(0, len(r)):
            val = r[i]

            val = val.replace("^10", "\n")

            if val[-2:] == '$$':
                val = val[0:len(val)-2]

            if val == '$':
                val = ''

            row.append(val.strip())

        pk = row[0]

        return Peilmerk(
            pk=pk,
            hoogte=row[1],
            jaar=int(row[2]),
            merk=int(row[3]),
            omschrijving=row[4],
            windrichting=row[5],
            muurvlak_x=int(row[6] or 0),
            muurvlak_y=int(row[7] or 0),
            rws_nummer=row[8],
            geometrie=GEOSGeometry(row[9]),
        )


class ImportNapJob(object):
    name = "Import NAP"

    def __init__(self):
        diva = settings.DIVA_DIR
        if not os.path.exists(diva):
            raise ValueError("DIVA_DIR not found: {}".format(diva))

        self.nap = os.path.join(diva, 'nap')

    def tasks(self):
        return [
            ImportNapTask(self.nap)
        ]
