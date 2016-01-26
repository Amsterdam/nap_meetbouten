from datapunt_generic.generic import rest
from . import models


class MeetboutenMixin(rest.DataSetSerializerMixin):
    dataset = 'meetbouten'


# list serializers
class Meetbout(MeetboutenMixin, rest.HALSerializer):
    _display = rest.DisplayField()

    class Meta:
        model = models.Meetbout
        fields = (
            '_links',
            '_display',
            'id',
        )


class Meting(MeetboutenMixin, rest.HALSerializer):
    _display = rest.DisplayField()

    class Meta:
        model = models.Meting
        fields = (
            '_links',
            '_display',
            'id',
        )


class Referentiepunt(MeetboutenMixin, rest.HALSerializer):
    _display = rest.DisplayField()

    class Meta:
        model = models.Referentiepunt
        fields = (
            '_links',
            '_display',
            'locatie',
        )


class Rollaag(MeetboutenMixin, rest.HALSerializer):
    _display = rest.DisplayField()

    class Meta:
        model = models.Rollaag
        fields = (
            '_links',
            '_display',
            'id',
        )


# detail serializers
class MeetboutDetail(MeetboutenMixin, rest.HALSerializer):
    _display = rest.DisplayField()

    class Meta:
        model = models.Meetbout
        fields = (
            '_links',
            '_display',

            'id',
            'locatie_x',
            'locatie_y',
            'bouwblokzijde',
            'blokeenheid',
            'status',
            'beveiligd',
            'eigenaar',
            'nabij_adres',
            'bouwbloknummer',
            'stadsdeel_code',
        )


class MetingDetail(MeetboutenMixin, rest.HALSerializer):
    meetbout = rest.RelatedSummaryField()
    _display = rest.DisplayField()

    class Meta:
        model = models.Meetbout
        fields = (
            '_links',
            '_display',

            'id',
            'type',
            'datum',
            'dagen_vorige_meting',
            'hoogte',
            'zakking',
            'zakkingssnelheid',
            'zakking_cumulatief',
            'ingewonnen',
            'meetbout',
            'refereert_aan',
            'gemeten_door',
        )


class ReferentiepuntDetail(MeetboutenMixin, rest.HALSerializer):
    peilmerk = rest.RelatedSummaryField()
    _display = rest.DisplayField()

    class Meta:
        model = models.Referentiepunt
        fields = (
            '_links',
            '_display',

            'locatie',
            'locatie_x',
            'locatie_y',
            'hoogte',
            'datum',
            'peilmerk',
            'geometrie',
        )


class RollaagDetail(MeetboutenMixin, rest.HALSerializer):
    meetbout = rest.RelatedSummaryField()
    _display = rest.DisplayField()

    class Meta:
        model = models.Referentiepunt
        fields = (
            '_links',
            '_display',

            'id',
            'meetbout',
            'geometrie',
        )
