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


class PeilViewSet(rest.AtlasViewSet):
    """
    """

    metadata_class = ExpansionMetadata
    queryset = models.Peilmerk.objects.all()
    serializer_detail_class = serializers.PeilmerkDetail
    serializer_class = serializers.Peilmerk
    filter_fields = ('omschrijving',)
