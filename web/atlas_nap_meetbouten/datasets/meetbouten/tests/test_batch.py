from datapunt_generic.batch.test import TaskTestCase
from .. import batch, models

NAP = 'diva/meetbouten'


class ImportMeetboutenTest(TaskTestCase):
    def task(self):
        return batch.ImportMeetboutenTask(NAP)

    def test_import(self):
        self.run_task()

        imported = models.Meetbout.objects.all()
        self.assertEqual(len(imported), 100)

        meetbout = models.Meetbout.objects.get(pk='10381494')
        self.assertEqual(meetbout.nabij_adres, 'Nassaukade 300')
