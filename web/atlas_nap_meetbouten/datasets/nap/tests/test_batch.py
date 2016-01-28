from datapunt_generic.batch.test import TaskTestCase
from .. import batch, models

NAP = 'diva/nap'


class ImportNapTest(TaskTestCase):
    def task(self):
        return batch.ImportNapTask(NAP)

    def test_import(self):
        self.run_task()

        imported = models.Peilmerk.objects.all()
        self.assertEqual(len(imported), 639)

        a = models.Peilmerk.objects.get(pk='10480009')
        self.assertEqual(a.omschrijving, 'Spuistraat 94')
