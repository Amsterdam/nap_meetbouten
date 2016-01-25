# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

from geo_views import migrate


class Migration(migrations.Migration):
    dependencies = [
        ('nap', '0002_auto_20160124_1817')
    ]

    operations = [
        migrate.ManageView(view_name="geo_nap_peilmerk", sql="SELECT id, hoogte, geometrie FROM nap_peilmerk"),
    ]
