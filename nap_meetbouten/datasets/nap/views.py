from rest_framework import metadata
from django_filters.rest_framework import DjangoFilterBackend

from datapunt_api import rest
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


class PeilViewSet(rest.DatapuntViewSet):
    """
    Peilmerken. Het Amsterdams Peil (meestal afgekort tot NAP)
    is de referentiehoogte waaraan hoogtemetingen in Nederland
    worden gerelateerd. Het NAP-net bestaat uit ongeveer 50.000
    zichtbare peilmerken en 250 ondergrondse peilmerken in
    Nederland, waarvan ongeveer 1000 in Amsterdam.
    """
    metadata_class = ExpansionMetadata
    queryset = models.Peilmerk.objects.all().order_by('id')
    serializer_detail_class = serializers.PeilmerkDetail
    serializer_class = serializers.Peilmerk
    filter_fields = ('omschrijving', 'merk', 'jaar', 'hoogte', 'rws_nummer')

    filter_backends = (DjangoFilterBackend,)
