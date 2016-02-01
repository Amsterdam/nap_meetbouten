from django.core.management import BaseCommand

from django.conf import settings

import datasets

import datasets.meetbouten.batch
import datasets.nap.batch

from datapunt_generic.batch import batch


class Command(BaseCommand):

    ordered = ['nap', 'meetbouten']

    indexes = dict(
        meetbouten=[datasets.meetbouten.batch.IndexMeetboutenJob],
        #nap=[datasets.nap.batch.IndexNapJob],
        nap=[]
    )

    backup_indexes = dict(
        meetbouten=[datasets.meetbouten.batch.BackupMeetboutenJob],
        #nap=[datasets.nap.batch.BackupNapJob],
        nap=[]
    )

    restore_indexes = dict(
        meetbouten=[datasets.meetbouten.batch.RestoreMeetboutenJob],
        #nap=[datasets.nap.batch.RestoreNapJob],
        nap=[]
    )

    def add_arguments(self, parser):
        parser.add_argument(
            'dataset',
            nargs='*',
            default=self.ordered,
            help="Dataset to use, choose from {}".format(
                ', '.join(self.indexes.keys())))

        parser.add_argument('--backup',
                            action='store_true',
                            dest='backup_indexes_es',
                            default=False,
                            help='Backup elsatic search')

        parser.add_argument('--restore',
                            action='store_true',
                            dest='restore_indexes_es',
                            default=False,
                            help='Restore elsatic search index')

        parser.add_argument('--build',
                            action='store_true',
                            dest='build_index',
                            default=False,
                            help='Build elastic index from postgres')

        parser.add_argument('--batch-size', default='10000', type=int,
                            help='Change batch size on inport')

    def handle(self, *args, **options):
        dataset = options['dataset']

        for ds in dataset:
            if ds not in self.indexes.keys():
                self.stderr.write("Unkown dataset: {}".format(ds))
                return

        sets = [ds for ds in self.ordered if ds in dataset]     # enforce order

        self.stdout.write("Working on {}".format(", ".join(sets)))

        if options['batch_size'] > 0:
            settings.BATCH_SETTINGS['batch_size'] = options['batch_size']

        for ds in sets:

            if options['backup_indexes_es']:
                for job_class in self.backup_indexes[ds]:
                    batch.execute(job_class())
                # we do not run the other tasks
                continue  # to next dataset please..

            if options['restore_indexes_es']:
                for job_class in self.restore_indexes[ds]:
                    batch.execute(job_class())
                # we do not run the other tasks
                continue  # to next dataset please..

            if options['build_index']:
                for job_class in self.indexes[ds]:
                    batch.execute(job_class())
