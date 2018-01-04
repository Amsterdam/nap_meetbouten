# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings

from django.db import migrations

from geo_views import migrate

URL = settings.DATAPUNT_API_URL


class Migration(migrations.Migration):
    dependencies = [
        ('meetbouten', '0008_auto_20160511_0844'),
        ('nap', '0003_auto_20160127_1246'),
    ]

    operations = [
        migrate.ManageView(
            view_name="geo_meetbouten_meetbout",
            sql=f"""
SELECT
    mb.id,
    mb.id as display,
    mb.status,
    mb.zakkingssnelheid,
    'meetbouten/meetbout'::TEXT AS type,
    '{URL}' || 'meetbouten/meetbout/' || mb.id || '/' AS uri,
    mb.geometrie
FROM meetbouten_meetbout mb
WHERE
    ST_IsValid(mb.geometrie)
"""
        ),

        migrate.ManageView(
            view_name="geo_meetbouten_referentiepunt",
            sql=f"""
SELECT
    rp.id,
    rp.id as display,
    rp.hoogte_nap,
    'meetbouten/referentiepunt'::TEXT AS type,
    '{URL}' || 'meetbouten/referentiepunt/' || rp.id || '/' AS uri,
    rp.geometrie
FROM
    meetbouten_referentiepunt rp
WHERE
    ST_IsValid(rp.geometrie)
"""
        ),

        migrate.ManageView(
            view_name="geo_nap_peilmerk",
            sql=f"""
SELECT
    pm.id,
    pm.id as display,
    pm.hoogte,
    'nap/peilmerk'::TEXT AS type,
    '{URL}' || 'nap/peilmerk/' || pm.id || '/' AS uri,
    pm.geometrie
FROM
    nap_peilmerk pm
WHERE
    pm.geometrie IS NOT NULL
            """),
    ]
