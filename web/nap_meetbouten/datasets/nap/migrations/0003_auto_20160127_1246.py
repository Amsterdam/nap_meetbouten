# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('nap', '0002_auto_20160126_1456'),
    ]

    operations = [
        migrations.AlterField(
            model_name='peilmerk',
            name='merk',
            field=models.SmallIntegerField(null=True, choices=[
                (0, 'ronde bout met opschrift NAP (0)'), (1,
                                                          'ronde bout (aan de bovenzijde) zonder opschrift of met opschrift anders dan NAP (1)'),
                (2, 'kleine ronde bout (2)'), (3, 'knopbout (3)'),
                (4, 'vierkante bout met of zonder groeven (4)'),
                (5, 'kleine ronde kruisbout (5)'), (7,
                                                    'bijzondere merktekens, bijvoorbeeld zeskantige bout, stalen pen, enz. (7)'),
                (13, 'kopbout (13)'), (14,
                                       'inbusbout (cilinderschroef met binnen zeskant) in slaganker M6 (14)'),
                (15, 'koperen hakkelbout (15)'), (16, 'koperen bout (16)'),
                (17, 'RVS-bout (17)'),
                (18, 'koperen bout met 3 Andreas kruizen (18)'),
                (99, 'onbekend (99)')]),
        ),
    ]
