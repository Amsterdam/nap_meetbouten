# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):
    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Peilmerk',
            fields=[
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('id', models.CharField(serialize=False, primary_key=True,
                                        max_length=10)),
                ('hoogte', models.DecimalField(decimal_places=4, max_digits=10,
                                               null=True)),
                ('jaar', models.IntegerField(null=True)),
                ('merk', models.SmallIntegerField(
                    choices=[(0, 'ronde bout met opschrift NAP'), (1,
                                                                   'ronde bout (aan de bovenzijde) zonder opschrift of met opschrift anders dan NAP'),
                             (2, 'kleine ronde bout'), (3, 'knopbout'),
                             (4, 'vierkante bout met of zonder groeven'),
                             (5, 'kleine ronde kruisbout'), (7,
                                                             'bijzondere merktekens, bijvoorbeeld zeskantige bout, stalen pen, enz.'),
                             (13, 'kopbout'), (14,
                                               'inbusbout (cilinderschroef met binnen zeskant) in slaganker M6'),
                             (15, 'koperen hakkelbout'), (16, 'koperen bout'),
                             (17, 'RVS-bout'),
                             (18, 'koperen bout met 3 Andreas kruizen'),
                             (99, 'onbekend')])),
                ('omschrijving', models.TextField(null=True)),
                ('windrichting', models.CharField(max_length=2, null=True)),
                ('muurvlak_x', models.IntegerField(null=True)),
                ('muurvlak_y', models.IntegerField(null=True)),
                ('geometrie',
                 django.contrib.gis.db.models.fields.PointField(null=True,
                                                                srid=28992)),
                ('rws_nummer', models.CharField(max_length=10, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
