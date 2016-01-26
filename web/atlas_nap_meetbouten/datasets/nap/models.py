from django.db import models
from django.contrib.gis.db import models as geo

from datapunt_generic.generic import mixins


class Peilmerk(mixins.ImportStatusMixin):
    MERK_0 = 0
    MERK_1 = 1
    MERK_2 = 2
    MERK_3 = 3
    MERK_4 = 4
    MERK_5 = 5
    MERK_7 = 7
    MERK_13 = 13
    MERK_14 = 14
    MERK_15 = 15
    MERK_16 = 16
    MERK_17 = 17
    MERK_18 = 18
    MERK_99 = 99

    MERK_CHOICES = (
        (MERK_0, "ronde bout met opschrift NAP"),
        (MERK_1, "ronde bout (aan de bovenzijde) zonder opschrift of met opschrift anders dan NAP"),
        (MERK_2, "kleine ronde bout"),
        (MERK_3, "knopbout"),
        (MERK_4, "vierkante bout met of zonder groeven"),
        (MERK_5, "kleine ronde kruisbout"),
        (MERK_7, "bijzondere merktekens, bijvoorbeeld zeskantige bout, stalen pen, enz."),
        (MERK_13, "kopbout"),
        (MERK_14, "inbusbout (cilinderschroef met binnen zeskant) in slaganker M6"),
        (MERK_15, "koperen hakkelbout"),
        (MERK_16, "koperen bout"),
        (MERK_17, "RVS-bout"),
        (MERK_18, "koperen bout met 3 Andreas kruizen"),
        (MERK_99, "onbekend"),
    )

    id = models.CharField(max_length=10, primary_key=True)
    hoogte = models.DecimalField(decimal_places=4, max_digits=10, null=True)
    jaar = models.IntegerField(null=True)
    merk = models.SmallIntegerField(choices=MERK_CHOICES, null=True)
    omschrijving = models.TextField(null=True)
    windrichting = models.CharField(max_length=2, null=True)
    muurvlak_x = models.IntegerField(null=True)
    muurvlak_y = models.IntegerField(null=True)
    geometrie = geo.PointField(null=True, srid=28992)
    rws_nummer = models.CharField(max_length=10, null=True)

    objects = geo.GeoManager()
