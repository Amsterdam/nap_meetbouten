# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Meetbout',
            fields=[
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('buurt', models.CharField(max_length=50, null=True)),
                ('locatie_x', models.DecimalField(max_digits=10, decimal_places=2, null=True)),
                ('locatie_y', models.DecimalField(max_digits=10, decimal_places=2, null=True)),
                ('hoogte_nap', models.DecimalField(max_digits=7, null=True, decimal_places=4)),
                ('zakking_cumulatief', models.DecimalField(max_digits=20, null=True, decimal_places=13)),
                ('datum', models.DateField(null=True)),
                ('bouwblokzijde', models.CharField(max_length=10, null=True)),
                ('eigenaar', models.CharField(max_length=50, null=True)),
                ('beveiligd', models.BooleanField(default=False)),
                ('deelraad', models.CharField(max_length=50, null=True)),
                ('nabij_adres', models.CharField(max_length=255, null=True)),
                ('locatie', models.CharField(max_length=50, null=True)),
                ('zakkingssnelheid', models.DecimalField(max_digits=20, null=True, decimal_places=13)),
                ('status', models.CharField(max_length=1, choices=[('A', 'actueel'), ('V', 'vervallen')], null=True)),
                ('bouwbloknummer', models.CharField(max_length=4, null=True)),
                ('blokeenheid', models.SmallIntegerField(null=True)),
                ('geometrie', django.contrib.gis.db.models.fields.PointField(srid=28992, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Meting',
            fields=[
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('datum', models.DateField(null=True)),
                ('type', models.CharField(max_length=1, choices=[('N', 'nulmeting'), ('H', 'herhalingsmeting'), ('T', 'tussentijdse meting'), ('S', 'schatting')], null=True)),
                ('hoogte_nap', models.DecimalField(max_digits=7, null=True, decimal_places=4)),
                ('zakking', models.DecimalField(max_digits=20, null=True, decimal_places=13)),
                ('zakkingssnelheid', models.DecimalField(max_digits=20, null=True, decimal_places=13)),
                ('zakking_cumulatief', models.DecimalField(max_digits=20, null=True, decimal_places=13)),
                ('ploeg', models.CharField(max_length=50)),
                ('type_int', models.SmallIntegerField(null=True)),
                ('dagen_vorige_meting', models.IntegerField(default=0)),
                ('pandmsl', models.CharField(max_length=50, null=True)),
                ('deelraad', models.CharField(max_length=50, null=True)),
                ('wvi', models.CharField(max_length=50, null=True)),
                ('meetbout', models.ForeignKey(to='meetbouten.Meetbout')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Referentiepunt',
            fields=[
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('locatie_x', models.DecimalField(max_digits=10, decimal_places=2, null=True)),
                ('locatie_y', models.DecimalField(max_digits=10, decimal_places=2, null=True)),
                ('hoogte_nap', models.DecimalField(max_digits=7, null=True, decimal_places=4)),
                ('datum', models.DateField(null=True)),
                ('locatie', models.CharField(max_length=255, null=True)),
                ('geometrie', django.contrib.gis.db.models.fields.PointField(srid=28992, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Rollaag',
            fields=[
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('locatie_x', models.DecimalField(max_digits=10, decimal_places=2, null=True)),
                ('locatie_y', models.DecimalField(max_digits=10, decimal_places=2, null=True)),
                ('geometrie', django.contrib.gis.db.models.fields.PointField(srid=28992, null=True)),
                ('meetbout', models.ForeignKey(to='meetbouten.Meetbout')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='meting',
            name='refereert_aan',
            field=models.ManyToManyField(to='meetbouten.Referentiepunt'),
        ),
    ]
