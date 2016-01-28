# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nap', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='peilmerk',
            name='merk',
            field=models.SmallIntegerField(choices=[(0, 'ronde bout met opschrift NAP'), (1, 'ronde bout (aan de bovenzijde) zonder opschrift of met opschrift anders dan NAP'), (2, 'kleine ronde bout'), (3, 'knopbout'), (4, 'vierkante bout met of zonder groeven'), (5, 'kleine ronde kruisbout'), (7, 'bijzondere merktekens, bijvoorbeeld zeskantige bout, stalen pen, enz.'), (13, 'kopbout'), (14, 'inbusbout (cilinderschroef met binnen zeskant) in slaganker M6'), (15, 'koperen hakkelbout'), (16, 'koperen bout'), (17, 'RVS-bout'), (18, 'koperen bout met 3 Andreas kruizen'), (99, 'onbekend')], null=True),
        ),
    ]
