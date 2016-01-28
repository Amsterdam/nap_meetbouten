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

        meetbout = models.Meetbout.objects.get(pk='11081251')
        self.assertEqual(meetbout.nabij_adres, 'Wenslauerstraat 48')


class ImportReferentiepuntenTest(TaskTestCase):
    def task(self):
        return batch.ImportReferentiepuntenTask(NAP)

    def test_import(self):
        self.run_task()

        imported = models.Referentiepunt.objects.all()
        self.assertEqual(len(imported), 389)

        referentiepunt = models.Referentiepunt.objects.get(pk='12489014')
        self.assertEqual(referentiepunt.locatie, 'Insulindeweg 71A-M')
