from rest_framework import serializers

from datapunt_api.serializers import DisplayField
from datapunt_api.serializers import HALSerializer
from datapunt_api.serializers import DataSetSerializerMixin as DS

from . import models


class Peilmerk(DS, HALSerializer):
    _display = DisplayField()
    dataset = 'nap'

    class Meta:
        model = models.Peilmerk
        fields = (
            '_links',
            '_display',
            'id',
        )


class PeilmerkDetail(DS, HALSerializer):
    dataset = 'nap'
    merk = serializers.CharField(source='get_merk_display')
    _display = DisplayField()

    peilmerkidentificatie = serializers.CharField(source='id')
    hoogte_nap = serializers.CharField(source='hoogte')
    x_muurvlak = serializers.CharField(source='muurvlak_x')
    y_muurvlak = serializers.CharField(source='muurvlak_y')

    class Meta:
        model = models.Peilmerk
        fields = (
            '_links',
            '_display',
            'peilmerkidentificatie',
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
