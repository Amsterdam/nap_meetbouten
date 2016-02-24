from django.db import connection

from django.contrib.gis.geos import Point
from django.test import TestCase
from datasets.nap.tests import factories as nap_factories
from datasets.meetbouten.tests import factories as meetbouten_factories

point = Point(0.0, 1.1)


class ViewsTest(TestCase):
    def get_row(self, view_name):
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM " + str(view_name) + " LIMIT 1")
        result = cursor.fetchone()
        self.assertIsNotNone(result)

        return dict(zip([col[0] for col in cursor.description], result))

    def test_nap_peilmerk_no_geo(self):
        nap_factories.PeilmerkFactory.create()
        with(self.assertRaises(AssertionError)):
            self.get_row('geo_nap_peilmerk')

    def test_nap_peilmerk(self):
        l = nap_factories.PeilmerkFactory.create(geometrie=point)
        row = self.get_row('geo_nap_peilmerk')
        self.assertEqual(row['id'], l.id)
        self.assertIn(l.id, row['display'])
        self.assertIn("geometrie", row)
        self.assertEqual(row['uri'],
                         'http://update.me/nap/peilmerk/{}/'.format(l.id))

    def test_meetbouten_meetbout_no_geo(self):
        meetbouten_factories.MeetboutFactory.create()
        with(self.assertRaises(AssertionError)):
            self.get_row('geo_meetbouten_meetbout')

    def test_meetbouten_meetbout(self):
        mb = meetbouten_factories.MeetboutFactory.create(geometrie=point)
        row = self.get_row('geo_meetbouten_meetbout')
        self.assertEqual(row['id'], mb.id)
        self.assertIn(mb.id, row['display'])
        self.assertIn("geometrie", row)
        self.assertEqual(row['uri'],
                         'http://update.me/meetbouten/meetbout/{}/'.format(mb.id))

    def test_meetbouten_referentiepunt_no_geo(self):
        meetbouten_factories.ReferentiepuntFactory.create()
        with(self.assertRaises(AssertionError)):
            self.get_row('geo_meetbouten_referentiepunt')

    def test_meetbouten_referentiepunt(self):
        rp = meetbouten_factories.ReferentiepuntFactory.create(geometrie=point)
        row = self.get_row('geo_meetbouten_referentiepunt')
        self.assertEqual(row['id'], rp.id)
        self.assertIn(rp.id, row['display'])
        self.assertIn("geometrie", row)
        self.assertEqual(row['uri'],
                         'http://update.me/meetbouten/referentiepunt/{}/'.format(rp.id))
