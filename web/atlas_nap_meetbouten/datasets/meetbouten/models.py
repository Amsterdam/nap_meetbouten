from django.db import models
from django.conf import settings
from django.contrib.gis.db import models as geo

from datapunt_generic.generic import mixins

from datasets.nap.models import Peilmerk


# $$12281260$$|
# $$$$|
# 123258|
# 485769|
# 1,1186|
# 17,6000000000001|
# $$19941128$$|
# 5|
# |
# $$N$$|
# $$M$$|
# $$Oosterpark 51$$|
# $$$$|
# 3,58082497212933|
# $$A$$|
# $$AN25 $$|
# 4|
# POINT (123258.0 485769.0)
class Meetbout(mixins.ImportStatusMixin):
    STATUS_ACTUEEL = 'A'
    STATUS_VERVALLEN = 'V'

    STATUS_CHOICES = (
        (STATUS_ACTUEEL, 'actueel'),
        (STATUS_VERVALLEN, 'vervallen'),
    )

    id = models.CharField(max_length=10, primary_key=True)
    buurt = models.CharField(max_length=50, null=True)
    locatie_x = models.IntegerField(null=True)
    locatie_y = models.IntegerField(null=True)
    hoogte_nap = models.DecimalField(
            max_digits=settings.NAP_MAX_DIGITS,
            decimal_places=settings.NAP_DECIMAL_PLACES,
            null=True
    )
    zakking_cumulatief = models.DecimalField(
            max_digits=settings.ZAKKING_MAX_DIGITS,
            decimal_places=settings.ZAKKING_DECIMAL_PLACES,
            null=True
    )
    datum = models.DateField(null=True)
    bouwblokzijde = models.CharField(max_length=10, null=True)
    eigenaar = models.CharField(max_length=50, null=True)
    beveiligd = models.BooleanField(default=False)
    deelraad = models.CharField(max_length=50, null=True)
    nabij_adres = models.CharField(max_length=255, null=True)
    locatie = models.CharField(max_length=50, null=True)
    zakkingssnelheid = models.DecimalField(
            max_digits=settings.ZAKKING_MAX_DIGITS,
            decimal_places=settings.ZAKKING_DECIMAL_PLACES,
            null=True
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, null=True)
    bouwbloknummer = models.CharField(max_length=4, null=True)
    blokeenheid = models.SmallIntegerField(null=True)

    stadsdeel_code = models.CharField(max_length=3, null=True)


# 27391|
# $$19950814$$|
# $$H$$|
# ,9201|
# ,399999999999956|
# $$13781412$$|
# $$13789003$$|
# $$$$|
# $$$$|
# ,453416149068315|
# 1,19999999999998|
# $$Fugro$$|
# 6|
# 553|
# |
# $$K$$|
# $$W$$
class Meting(mixins.ImportStatusMixin):
    TYPE_NULMETING = 'N'
    TYPE_HERHALINGSMETING = 'H'
    TYPE_TUSSENTIJDS = 'T'
    TYPE_SCHATTING = 'S'

    TYPE_CHOICES = (
        (TYPE_NULMETING, 'nulmeting'),
        (TYPE_HERHALINGSMETING, 'herhalingsmeting'),
        (TYPE_TUSSENTIJDS, 'tussentijdse meting'),
        (TYPE_SCHATTING, 'schatting'),
    )

    id = models.CharField(max_length=10, primary_key=True)
    type = models.CharField(max_length=1, choices=TYPE_CHOICES)
    datum = models.DateField()
    dagen_vorige_meting = models.IntegerField(default=0)
    hoogte_nap = models.DecimalField(
            max_digits=settings.NAP_MAX_DIGITS,
            decimal_places=settings.NAP_DECIMAL_PLACES,
            null=True
    )
    zakking = models.IntegerField()
    zakkingssnelheid = models.DecimalField(
            max_digits=settings.ZAKKING_MAX_DIGITS,
            decimal_places=settings.ZAKKING_DECIMAL_PLACES,
            null=True
    )
    zakking_cumulatief = models.DecimalField(
            max_digits=settings.ZAKKING_MAX_DIGITS,
            decimal_places=settings.ZAKKING_DECIMAL_PLACES,
            null=True
    )
    ingewonnen = models.CharField(max_length=10)
    meetbout = models.ForeignKey(Meetbout)
    refereert_aan = models.ForeignKey('Referentiepunt')
    gemeten_door = models.CharField(max_length=50)


# $$13089003$$|
# 122586|
# 485483|
# 1,4186|
# $$19940318$$|
# $$Wibautstraat 87A/93H$$|
# POINT (122586.0 485483.0)
class Referentiepunt(mixins.ImportStatusMixin):
    locatie = models.CharField(max_length=255)
    locatie_x = models.IntegerField()
    locatie_y = models.IntegerField()
    hoogte_nap = models.DecimalField(
            max_digits=settings.NAP_MAX_DIGITS,
            decimal_places=settings.NAP_DECIMAL_PLACES,
            null=True
    )
    datum = models.DateField()
    geometrie = geo.PointField(null=True, srid=28992)
    peilmerk = models.ForeignKey(Peilmerk)

    objects = geo.GeoManager()


# $$AK25$$|
# 1|
# 121287|
# 485235|
# POINT (121287.0 485245.0)
class Rollaag(mixins.ImportStatusMixin):
    id = models.IntegerField(primary_key=True)
    meetbout = models.ForeignKey(Meetbout)
    geometrie = geo.PointField(null=True, srid=28992)

    objects = geo.GeoManager()
