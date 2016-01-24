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
    _display = rest.DisplayField()

    class Meta:
        model = models.Peilmerk
        fields = (
            '_links',
            '_display',
            'id',
            'hoogte',
            'jaar',
            'merk',
            'omschrijving',
            'windrichting',
            'muurvlak_x',
            'muurvlak_y',
            'rws_nummer',
            'geometrie',
        )
