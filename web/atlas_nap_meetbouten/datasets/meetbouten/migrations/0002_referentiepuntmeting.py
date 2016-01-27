# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetbouten', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReferentiepuntMeting',
            fields=[
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('id', models.CharField(serialize=False, max_length=30, primary_key=True)),
                ('meting', models.ForeignKey(to='meetbouten.Meting')),
                ('referentiepunt', models.ForeignKey(to='meetbouten.Referentiepunt')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
