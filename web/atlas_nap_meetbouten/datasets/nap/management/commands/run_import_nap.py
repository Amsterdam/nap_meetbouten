from django.core.management import BaseCommand

import datasets.nap.batch

from datapunt_generic.batch import batch


class Command(BaseCommand):

    ordered = ['nap']

    imports = dict(
        nap=[datasets.nap.batch.ImportNapJob],
    )

    indexes = dict(
        nap=[],
    )

    backup_indexes = dict(
        nap=[],
    )

    restore_indexes = dict(
        nap=[],
    )

    def add_arguments(self, parser):
        parser.add_argument(
            'dataset',
            nargs='*',
            default=self.ordered,
            help="Dataset to import, choose from {}".format(
                ', '.join(self.imports.keys())))

        parser.add_argument('--backup-indexes-es',
                            action='store_true',
                            dest='backup_indexes_es',
                            default=False,
                            help='Backup elsatic search')

        parser.add_argument('--restore-indexes-es',
                            action='store_true',
                            dest='restore_indexes_es',
                            default=False,
                            help='Restore elsatic search index')

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

        parser.add_argument('--noinput', '--no-input',
                            action='store_false', dest='interactive', default=True,
                            help='Tells Django to NOT prompt the user for input of any kind.')

    def handle(self, *args, **options):
        dataset = options['dataset']

        for ds in dataset:
            if ds not in self.imports.keys():
                self.stderr.write("Unkown dataset: {}".format(ds))
                return

        sets = [ds for ds in self.ordered if ds in dataset]     # enforce order

        self.stdout.write("Importing {}".format(", ".join(sets)))

        for ds in sets:

            if options['run-import']:
                for job_class in self.imports[ds]:
                    batch.execute(job_class())

            if options['run-index']:
                for job_class in self.indexes[ds]:
                    batch.execute(job_class())
