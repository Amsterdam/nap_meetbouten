from rest_framework import serializers

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
    status = serializers.CharField(source='get_status_display')
    bouwblok = serializers.SerializerMethodField()
    rollaag = serializers.SerializerMethodField()
    _display = rest.DisplayField()

    class Meta:
        model = models.Meetbout
        fields = (
            '_links',
            '_display',

            'id',
            'buurt',
            'locatie_x',
            'locatie_y',
            'hoogte_nap',
            'zakking_cumulatief',
            'datum',
            'bouwblokzijde',
            'eigenaar',
            'beveiligd',
            'deelraad',
            'nabij_adres',
            'locatie',
            'zakkingssnelheid',
            'status',
            'bouwblok',
            'bouwbloknummer',
            'blokeenheid',
            'rollaag',
            'geometrie',
        )

    def get_bouwblok(self, obj):
        link = "/gebieden/bouwblok/{}".format(obj.bouwbloknummer)
        req = self.context.get('request')
        if req:
            link = req.build_absolute_uri(link)
        return link

    def get_rollaag(self, obj):
        if obj.bouwbloknummer:
            return 'http://atlas.amsterdam.nl/rollagen/{}.jpg'.format(obj.bouwbloknummer.lower())

        return None


class ReferentiepuntDetail(MeetboutenMixin, rest.HALSerializer):
    metingen = rest.RelatedSummaryField()
    _display = rest.DisplayField()

    class Meta:
        model = models.Referentiepunt
        fields = (
            '_links',
            '_display',

            'id',
            'locatie',
            'locatie_x',
            'locatie_y',
            'hoogte_nap',
            'datum',
            'locatie',
            'metingen',
            'geometrie',
        )


class MetingDetail(MeetboutenMixin, rest.HALSerializer):
    type = serializers.CharField(source='get_type_display')
    _display = rest.DisplayField()

    class Meta:
        model = models.Meting
        fields = (
            '_links',
            '_display',

            'id',
            'datum',
            'type',
            'hoogte_nap',
            'zakking',
            'meetbout',
            'zakkingssnelheid',
            'zakking_cumulatief',
            'ploeg',
            'dagen_vorige_meting',
        )


class RollaagDetail(MeetboutenMixin, rest.HALSerializer):
    _display = rest.DisplayField()

    class Meta:
        model = models.Rollaag
        fields = (
            '_links',
            '_display',

            'id',
            'meetbout',
            'locatie_x',
            'locatie_y',
            'geometrie',
        )
