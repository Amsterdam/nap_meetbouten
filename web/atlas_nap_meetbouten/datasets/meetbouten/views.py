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
    """

    metadata_class = ExpansionMetadata
    queryset = models.Meetbout.objects.all()
    serializer_detail_class = serializers.MeetboutDetail
    serializer_class = serializers.Meetbout
    filter_fields = ()


class MetingViewSet(rest.AtlasViewSet):
    """
    """

    metadata_class = ExpansionMetadata
    queryset = models.Meting.objects.all()
    serializer_detail_class = serializers.MetingDetail
    serializer_class = serializers.Meting
    filter_fields = ()


class ReferentiepuntViewSet(rest.AtlasViewSet):
    """
    """

    metadata_class = ExpansionMetadata
    queryset = models.Referentiepunt.objects.all()
    serializer_detail_class = serializers.ReferentiepuntDetail
    serializer_class = serializers.Referentiepunt
    filter_fields = ()


class RollaagViewSet(rest.AtlasViewSet):
    """
    """

    metadata_class = ExpansionMetadata
    queryset = models.Rollaag.objects.all()
    serializer_detail_class = serializers.RollaagDetail
    serializer_class = serializers.Rollaag
    filter_fields = ()

