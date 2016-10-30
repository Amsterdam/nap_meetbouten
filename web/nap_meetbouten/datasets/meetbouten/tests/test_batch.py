from . import factories

from datapunt_generic.batch.test import TaskTestCase
from .. import batch, models

NAP = 'diva/meetbouten'


class ImportMeetboutenTest(TaskTestCase):
    def setUp(self):
        self.laag_ad24 = factories.RollaagFactory.create(bouwblok='AD24')

    def task(self):
        return batch.ImportMeetboutTask(NAP)

    def test_import(self):
        self.run_task()

        imported = models.Meetbout.objects.all()
        self.assertEqual(len(imported), 100)

        meetbout = models.Meetbout.objects.get(pk='11081251')
        self.assertEqual(meetbout.adres, 'Wenslauerstraat 48')
        self.assertEqual(meetbout.rollaag, self.laag_ad24)


class ImportReferentiepuntenTest(TaskTestCase):
    def task(self):
        return batch.ImportReferentiepuntTask(NAP)

    def test_import(self):
        self.run_task()

        imported = models.Referentiepunt.objects.all()
        self.assertEqual(len(imported), 389)

        referentiepunt = models.Referentiepunt.objects.get(pk='12489014')
        self.assertEqual(referentiepunt.locatie, 'Insulindeweg 71A-M')


class ImportMetingTest(TaskTestCase):
    def setUp(self):
        factories.MeetboutFactory.create(pk='13681052')
        factories.MeetboutFactory.create(pk='11981059')
        factories.ReferentiepuntFactory.create(pk='11989006')
        factories.ReferentiepuntFactory.create(pk='11989007')

    def task(self):
        return batch.ImportMetingTask(NAP)

    def test_import(self):
        self.run_task()

        imported = models.Meting.objects.all()
        self.assertEqual(len(imported), 2)

        meting = models.Meting.objects.get(pk='31410')
        self.assertEqual(meting.type, models.Meting.TYPE_HERHALINGSMETING)
        self.assertEqual(len(meting.refereert_aan.all()), 2)


class ImportRollaagTest(TaskTestCase):
    def task(self):
        return batch.ImportRollaagTask(NAP)

    def test_import(self):
        self.run_task()

        imported = models.Rollaag.objects.all()
        self.assertEqual(len(imported), 436)
        self.assertEqual(imported[0].bouwblok, 'AK25')
