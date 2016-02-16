from rest_framework import metadata

from datapunt_generic.generic import rest
from . import serializers, models


class ExpansionMetadata(metadata.SimpleMetadata):
    def determine_metadata(self, request, view):
        result = super().determine_metadata(request, view)
        result['parameters'] = dict(
                full=dict(
                        type="string",
                        description="If present, related entities are inlined",
                        required=False
                )
        )
        return result


class MeetboutViewSet(rest.AtlasViewSet):
    """
    De meetbouten (roestvast stalen boutjes met een doorsnede van 6 mm) zijn op ongeveer een halve meter van het
    maaiveld geplaatst in de gevel.

    Meetbouten worden, op aanwijzing van het stadsdeel, met een zekere regelmaat geplaatst in verschillende panden. In
    gebieden die naar verwachting meer met funderingsproblemen te maken krijgen, worden extra meetbouten geplaatst. De
    verkregen meetgegevens zijn onderling vergelijkbaar. Er zijn ongeveer 13.000 bouten geplaatst. Het plaatsen van een
    meetbout heeft nagenoeg geen gevolgen voor het pand. Er wordt slechts een klein gaatje in een gevelsteen geboord.
    """

    metadata_class = ExpansionMetadata
    queryset = models.Meetbout.objects.all()
    serializer_detail_class = serializers.MeetboutDetail
    serializer_class = serializers.Meetbout
    filter_fields = ('bouwbloknummer', )


class MetingViewSet(rest.AtlasViewSet):
    """
    De meetbouten worden ten opzichte van een vast punt 'ingemeten', zodat de hoogte vastgesteld kan worden. De eerste
    meting, de zogenaamde nulmeting, is het uitgangspunt voor het beoordelen van eventuele deformatie (zakking). In
    principe zijn sindsdien drie herhalingsmetingen uitgevoerd. Het verschil tussen de nulmeting en de herhalingsmeting
    is een maat voor het zettingsgedrag.
    Soms vervallen meetbouten. Deze zijn om de een of andere reden niet meer aanwezig.
    """

    metadata_class = ExpansionMetadata
    queryset = models.Meting.objects.all()
    serializer_detail_class = serializers.MetingDetail
    serializer_class = serializers.Meting
    filter_fields = ('meetbout', 'refereert_aan__id')


class ReferentiepuntViewSet(rest.AtlasViewSet):
    """
    Voor de meting van meetbouten zijn zogenaamde referentiepunten aanwezig in de omgeving.
    """

    metadata_class = ExpansionMetadata
    queryset = models.Referentiepunt.objects.all()
    serializer_detail_class = serializers.ReferentiepuntDetail
    serializer_class = serializers.Referentiepunt
    filter_fields = ('metingen__id')


class RollaagViewSet(rest.AtlasViewSet):
    """
    Om de zakking van een heel bouwblok te bepalen worden rollagen gemeten. Een rollaag is een herkenbare laag in de
    bebouwing. Dit kan een doorlopende voeg zijn of een ander herkenbaar bouwkundig element.

    Op de plaats van de pandscheidingen wordt de hoogte van deze rollaag gemeten. Hierdoor ontstaat er een overzicht
    van de verzakking van een heel bouwblok.
    """

    metadata_class = ExpansionMetadata
    queryset = models.Rollaag.objects.all()
    serializer_detail_class = serializers.RollaagDetail
    serializer_class = serializers.Rollaag
    filter_fields = ('meetbout', )

