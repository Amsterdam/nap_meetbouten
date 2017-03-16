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
    straatnaam = es.Text(analyzer=analyzers.adres)

    meetboutnummer = es.Text(fielddata=True, analyzer=analyzers.boutnummer)

    _display = es.Text(index=False)

    subtype = es.Text(index=False)

    order = es.Integer()

    status = es.Text()

    locatie = es.Text(analyzer=analyzers.adres)

    x_coordinaat = es.Float()
    y_coordinaat = es.Float()

    hoogte_nap = es.Float()
    zakkingssnelheid = es.Float()

    beveiligd = es.Boolean()

    eigenaar = es.Text()

    bouwblokzijde = es.Text()
    bouwbloknummer = es.Text(analyzer=analyzers.boutnummer)

    adres = es.Text(analyzer=analyzers.adres)

    centroid = es.GeoPoint()

    class Meta:
        index = settings.ELASTIC_INDICES['MEETBOUTEN']


def from_meetbout(m: models.Meetbout):
    doc = Meetbout(_id=m.id)

    doc.meetboutnummer = m.id

    doc.subtype = 'meetbout'

    doc._display = m.id

    doc.status = m.status
    doc.locate = m.locatie

    doc.x_coordinaat = m.x_coordinaat
    doc.y_coordinaat = m.y_coordinaat

    doc.hoogte_nap = m.hoogte_nap
    doc.zakkingssnelheid = m.zakkingssnelheid

    doc.eigenaar = m.eigenaar

    doc.bouwbloknummer = m.bouwbloknummer

    doc.centroid = get_centroid(m.geometrie)

    doc.order = 100

    return doc
