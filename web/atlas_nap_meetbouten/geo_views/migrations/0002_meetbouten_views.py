# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

from geo_views import migrate


class Migration(migrations.Migration):
    dependencies = [
        ('meetbouten', '0001_initial'),
        ('geo_views', '0001_nap_views'),
    ]

    operations = [
        migrate.ManageView(
                view_name="geo_meetbouten_meetbout",
                sql="SELECT id, status, zakkingssnelheid, geometrie FROM meetbouten_meetbout"
        ),
        migrate.ManageView(
                view_name="geo_meetbouten_referentiepunt",
                sql="SELECT id, hoogte_nap,geometrie FROM meetbouten_referentiepunt"
        ),
    ]
