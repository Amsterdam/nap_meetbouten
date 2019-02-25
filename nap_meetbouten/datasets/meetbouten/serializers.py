from rest_framework import serializers

from datapunt_api.serializers import DisplayField
from datapunt_api.serializers import RelatedSummaryField
from datapunt_api.serializers import HALSerializer
from datapunt_api.serializers import DataSetSerializerMixin as DS

from . import models


# list serializers
class Meetbout(DS, HALSerializer):
    dataset = 'meetbouten'
    _display = DisplayField()

    class Meta:
        model = models.Meetbout
        fields = (
            '_links',
            '_display',
            'id',
        )


class Meting(DS, HALSerializer):
    dataset = 'meetbouten'
    _display = DisplayField()

    class Meta:
        model = models.Meting
        fields = (
            '_links',
            '_display',
            'id',
            'datum',
            'zakking',
            'hoogte_nap',
            'zakkingssnelheid',
            'zakking_cumulatief',
        )


class Referentiepunt(DS, HALSerializer):
    dataset = 'meetbouten'
    _display = DisplayField()

    class Meta:
        model = models.Referentiepunt
        fields = (
            '_links',
            '_display',
            'locatie',
        )


class Rollaag(DS, HALSerializer):
    dataset = 'meetbouten'
    _display = DisplayField()

    class Meta:
        model = models.Rollaag
        fields = (
            '_links',
            '_display',
            'id',
        )


# detail serializers
class MeetboutDetail(DS, HALSerializer):
    dataset = 'meetbouten'
    status = serializers.CharField(source='get_status_display')
    bouwblok_link = serializers.SerializerMethodField()
    stadsdeel_link = serializers.SerializerMethodField()
    metingen = RelatedSummaryField()
    _display = DisplayField()

    meetboutidentificatie = serializers.CharField(source='id')
    bouwblok = serializers.CharField(source='bouwbloknummer')

    class Meta:
        model = models.Meetbout
        fields = (
            '_links',
            '_display',

            'meetboutidentificatie',

            'buurt',
            'x_coordinaat',
            'y_coordinaat',
            'hoogte_nap',
            'zakking_cumulatief',
            'datum',
            'bouwblokzijde',
            'eigenaar',
            'beveiligd',
            'stadsdeel',
            'stadsdeel_link',
            'adres',
            'locatie',
            'zakkingssnelheid',
            'status',
            'bouwblok',
            'bouwblok_link',
            'blokeenheid',
            'rollaag',
            'metingen',
            'geometrie',
        )

    def get_bouwblok_link(self, obj):
        link = "/gebieden/bouwblok/{}".format(obj.bouwbloknummer)
        req = self.context.get('request')
        if req:
            link = req.build_absolute_uri(link)
        return link

    def get_stadsdeel_link(self, obj):
        link = "/gebieden/stadsdeel/{}".format(obj.stadsdeel)
        req = self.context.get('request')
        if req:
            link = req.build_absolute_uri(link)
        return link


class ReferentiepuntDetail(DS, HALSerializer):
    dataset = 'meetbouten'
    metingen = RelatedSummaryField()
    _display = DisplayField()

    referentiepuntidentificatie = serializers.CharField(source='id')

    class Meta:
        model = models.Referentiepunt
        fields = (
            '_links',
            '_display',

            'referentiepuntidentificatie',

            'locatie',

            'x_coordinaat',
            'y_coordinaat',

            'hoogte_nap',
            'datum',
            'locatie',
            'metingen',
            'geometrie',
        )


class MetingDetail(DS, HALSerializer):
    dataset = 'meetbouten'
    type = serializers.CharField(source='get_type_display')
    # refereert_aan = RelatedSummaryField()
    _display = DisplayField()

    metingidentificatie = serializers.CharField(source='id')
    aantal_dagen = serializers.CharField(source='dagen_vorige_meting')
    # referentiepunt = serializers.CharField(source='refereert_aan')
    referentiepunt = RelatedSummaryField(source='refereert_aan')
    onderneming = serializers.CharField(source='ploeg')

    class Meta:
        model = models.Meting
        fields = (
            '_links',
            '_display',

            'metingidentificatie',

            'datum',
            'type',
            'hoogte_nap',
            'zakking',
            'meetbout',
            'zakkingssnelheid',
            'zakking_cumulatief',
            'onderneming',
            'aantal_dagen',
            'referentiepunt',
        )


class RollaagDetail(DS, HALSerializer):
    dataset = 'meetbouten'
    afbeelding = serializers.SerializerMethodField()
    meetbouten = RelatedSummaryField()
    _display = DisplayField()

    rollaagidentificatie = serializers.CharField(source='id')

    class Meta:
        model = models.Rollaag
        fields = (
            '_links',
            '_display',

            'rollaagidentificatie',

            'meetbouten',

            'x_coordinaat',
            'y_coordinaat',

            'geometrie',
            'afbeelding',
        )

    def get_afbeelding(self, obj):
        if obj.bouwblok:
            return 'https://data.amsterdam.nl/rollagen/{}.jpg'.format(
                obj.bouwblok.lower())

        return None
