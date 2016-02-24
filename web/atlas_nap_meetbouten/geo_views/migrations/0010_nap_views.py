# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

from geo_views import migrate


class Migration(migrations.Migration):
    dependencies = [
        ('geo_views', '0009_meetbouten_views'),
    ]

    operations = [
        migrate.ManageView(
            view_name="geo_nap_peilmerk",
            sql="""
SELECT
    pm.id,
    pm.id as display,
    pm.hoogte,
    'nap/peilmerk' AS type,
    site.domain || 'nap/peilmerk/' || pm.id || '/' AS uri,
    pm.geometrie
FROM
    nap_peilmerk pm,
    django_site site
WHERE
    site.name = 'API Domain'
AND
    pm.geometrie IS NOT NULL
            """),
    ]
