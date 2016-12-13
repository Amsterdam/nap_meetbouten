from django.core.management import BaseCommand
from objectstore.objectstore import fetch_importfiles

import datasets.nap.batch
import datasets.meetbouten.batch

from datapunt_generic.batch import batch


class Command(BaseCommand):
    ordered = ['nap', 'meetbouten']

    imports = dict(
        nap=[datasets.nap.batch.ImportNapJob],
        meetbouten=[datasets.meetbouten.batch.ImportMeetboutenJob],
    )

    indexes = dict(
        nap=[],
        meetbouten=[datasets.meetbouten.batch.IndexMeetboutenJob],
    )

    def add_arguments(self, parser):
        parser.add_argument('dataset',
                            nargs='*',
                            default=self.ordered,
                            help="Dataset to import, choose from {}".format(
                                ', '.join(self.imports.keys())))

        parser.add_argument('--no-import',
                            action='store_false',
                            dest='run-import',
                            default=True,
                            help='Skip database importing')

        parser.add_argument('--no-index',
                            action='store_false',
                            dest='run-index',
                            default=True,
                            help='Skip elastic search indexing')

    def handle(self, *args, **options):
        dataset = options['dataset']

        for ds in dataset:
            if ds not in self.imports.keys():
                self.stderr.write("Unkown dataset: {}".format(ds))
                return

        sets = [ds for ds in self.ordered if ds in dataset]  # enforce order

        self.stdout.write("Importing {}".format(", ".join(sets)))

        for ds in sets:
            if options['run-import']:
                fetch_importfiles()
                for job_class in self.imports[ds]:
                    batch.execute(job_class())

            if options['run-index']:
                for job_class in self.indexes[ds]:
                    batch.execute(job_class())
