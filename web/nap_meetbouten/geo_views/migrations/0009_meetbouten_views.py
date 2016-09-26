# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

from geo_views import migrate


class Migration(migrations.Migration):
    dependencies = [
        ('geo_views', '0008_nap_views'),
    ]

    operations = [
        migrate.ManageView(
            view_name="geo_meetbouten_meetbout",
            sql="""
SELECT
    mb.id,
    mb.id as display,
    mb.status,
    mb.zakkingssnelheid,
    'meetbouten/meetbout' AS type,
    site.domain || 'meetbouten/meetbout/' || mb.id || '/' AS uri,
    mb.geometrie
FROM meetbouten_meetbout mb,
    django_site site
WHERE
    site.name = 'API Domain'
"""
        ),
        migrate.ManageView(
            view_name="geo_meetbouten_referentiepunt",
            sql="""
SELECT
    rp.id,
    rp.id as display,
    rp.hoogte_nap,
    'meetbouten/referentiepunt' AS type,
    site.domain || 'meetbouten/referentiepunt/' || rp.id || '/' AS uri,
    rp.geometrie
FROM
    meetbouten_referentiepunt rp,
    django_site site
WHERE
    site.name = 'API Domain'
"""
        ),
    ]
