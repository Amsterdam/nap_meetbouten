# Create your views here.

import logging

from django.conf import settings

from elasticsearch_dsl import Search, Q

from datapunt_generic.generic import SearchViewSet


log = logging.getLogger('search')


MEETBOUTEN = settings.ELASTIC_INDICES['MEETBOUTEN']


def mulitimatch_meetbout_Q(query):
    """
    Main 'One size fits all' search query used
    """
    log.debug('%20s %s', mulitimatch_meetbout_Q.__name__, query)

    return Q(
        "multi_match",
        query=query,
        # type="most_fields",
        # type="phrase",
        type="phrase_prefix",
        slop=12,     # match "stephan preeker" with "stephan jacob preeker"
        max_expansions=12,
        fields=[
            'naam',
            'straatnaam',
            'aanduiding',
            'adres',

            'locatie',
            'huisnummer'
            'huisnummer_variation',
        ]
    )


def add_sorting():
    """
    Give human understandable sorting to the output
    """
    return (
        # {"order": {
        #    "order": "asc", "missing": "_last", "unmapped_type": "long"}},
        # {"straatnaam": {
        #    "order": "asc", "missing": "_first", "unmapped_type": "string"}},
        # {"huisnummer": {
        #    "order": "asc", "missing": "_first", "unmapped_type": "long"}},
        # {"adres": {
        #    "order": "asc", "missing": "_first", "unmapped_type": "string"}},
        '-_score',
        # 'naam',
    )


def search_meetbout_query(view, client, query):
    """
    Execute search on adresses
    """
    return (
        Search(client)
        .index(MEETBOUTEN)
        .query(
            mulitimatch_meetbout_Q(query)
        )
        .sort(*add_sorting())
    )


class SearchAdresViewSet(SearchViewSet):
    """
    Given a query parameter `q`, this function returns a subset of
    all adressable objects that match the adres elastic search query.
    """
    url_name = 'search/meetbouten'
    search_query = search_meetbout_query
