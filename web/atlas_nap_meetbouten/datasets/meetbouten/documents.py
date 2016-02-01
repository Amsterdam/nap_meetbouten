import elasticsearch_dsl as es

from . import models

from datapunt_generic.generic import analyzers
from django.conf import settings


def get_centroid(geom):
    if not geom:
        return None

    result = geom.centroid
    result.transform('wgs84')
    return result.coords


class Meetbout(es.DocType):
    straatnaam = es.String(analyzer=analyzers.adres)

    status = es.String()

    locatie = es.String(analyzer=analyzers.adres)

    locatie_x = es.Float()
    locatie_y = es.Float()
    hoogte_nap = es.Float()
    zakkingssnelheid = es.Float()

    beveiligd = es.Boolean()

    eigenaar = es.String()
    bouwblokzijde = es.String()
    bouwbloknummer = es.String(analyzer=analyzers.adres)

    nabij_adres = es.String(analyzer=analyzers.adres)

    centroid = es.GeoPoint()

    class Meta:
        index = settings.ELASTIC_INDICES['MEETBOUTEN']


def from_meetbout(m: models.Meetbout):
    doc = Meetbout(_id=m.id)
    # add fields..

    doc.centroid = get_centroid(m.geometrie)

    return doc
