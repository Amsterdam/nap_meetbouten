# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def create_site(apps, *args, **kwargs):
    Site = apps.get_model('sites', 'Site')
    Site.objects.create(
        domain='http://update.me/',
        name='API Domain'
    )


def delete_site(apps, *args, **kwargs):
    Site = apps.get_model('sites', 'Site')
    Site.objects.filter(name='API Domain').delete()


class Migration(migrations.Migration):
    dependencies = [
        ('sites', '0001_initial'),
        ('geo_views', '0003_nap_views'),
    ]

    operations = [
        migrations.RunPython(code=create_site, reverse_code=delete_site)
    ]
