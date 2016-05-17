from rest_framework import serializers

from datapunt_generic.generic import rest
from . import models


class NapMixin(rest.DataSetSerializerMixin):
    dataset = 'nap'


class Peilmerk(NapMixin, rest.HALSerializer):
    _display = rest.DisplayField()

    class Meta:
        model = models.Peilmerk
        fields = (
            '_links',
            '_display',
            'id',
        )


class PeilmerkDetail(NapMixin, rest.HALSerializer):
    merk = serializers.CharField(source='get_merk_display')
    _display = rest.DisplayField()

    peilmerkidentificatie = serializers.CharField(source=id)
    hoogte_nap = serializers.CharField(source='hoogte')
    x_muurvlak = serializers.CharField(source='muurvlak_x')
    y_muurvlak = serializers.CharField(source='muurvlak_y')

    class Meta:
        model = models.Peilmerk
        fields = (
            '_links',
            '_display',
            'id',
            'hoogte_nap',
            'jaar',
            'merk',
            'omschrijving',
            'windrichting',
            'x_muurvlak',
            'y_muurvlak',
            'rws_nummer',
            'geometrie',
        )
