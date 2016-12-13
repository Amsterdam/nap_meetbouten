# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('meetbouten', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meting',
            name='dagen_vorige_meting',
            field=models.IntegerField(null=True, default=0),
        ),
    ]
