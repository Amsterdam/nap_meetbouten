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

    meetboutnummer = es.String(analyzer=analyzers.boutnummer)

    status = es.String()

    locatie = es.String(analyzer=analyzers.adres)

    locatie_x = es.Float()
    locatie_y = es.Float()
    hoogte_nap = es.Float()
    zakkingssnelheid = es.Float()

    beveiligd = es.Boolean()

    eigenaar = es.String()
    bouwblokzijde = es.String()
    bouwbloknummer = es.String(analyzer=analyzers.boutnummer)

    nabij_adres = es.String(analyzer=analyzers.adres)

    centroid = es.GeoPoint()

    class Meta:
        index = settings.ELASTIC_INDICES['MEETBOUTEN']


def from_meetbout(m: models.Meetbout):
    doc = Meetbout(_id=m.id)
    doc.meetboutnummer = m.id

    doc.status = m.status
    doc.locate = m.locatie

    doc.locatie_x = m.locatie_x
    doc.locatie_y = m.locatie_y
    doc.hoogte_nap = m.hoogte_nap
    doc.zakkingssnelheid = m.zakkingssnelheid

    doc.eigenaar = m.eigenaar

    doc.bouwbloknummer = m.bouwbloknummer

    doc.centroid = get_centroid(m.geometrie)

    return doc
