import datetime
import hashlib
import logging
import os
import csv

from django import db
from django.conf import settings

from datapunt_generic.batch import batch
from datapunt_generic.generic import geo, database, uva2

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
        with open(source) as f:
            rows = csv.reader(f, delimiter='|')
            self.peilmerken = [result for result in (self.process_row(row) for row in rows) if result]

        Peilmerk.objects.bulk_create(self.peilmerken.values(), batch_size=database.BATCH_SIZE)

    def process_row(self, r):
        pk = r[0]

        return pk, Peilmerk(
            pk=pk,
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
