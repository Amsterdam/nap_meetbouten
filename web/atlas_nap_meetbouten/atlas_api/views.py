# Create your views here.

import logging
from collections import OrderedDict

from django.conf import settings

from elasticsearch_dsl import Search, Q

from datapunt_generic.generic import searchviews
from datapunt_generic.generic import rest


log = logging.getLogger('search')


_details = {
    'meetbout': 'meetbout-detail',
}


def _get_url(request, hit):
    doc_type, id = hit.meta.doc_type, hit.meta.id

    if doc_type in _details:
        return rest.get_links(
            view_name=_details[doc_type],
            kwargs=dict(pk=id), request=request)


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
            "meetboutnummer",
            "bouwbloknummer",
            "locatie",
        ]
    )


def add_sorting():
    """
    Give human understandable sorting to the output
    """
    return (
        {"meetboutnummer": {
            "order": "asc", "missing": "_first", "unmapped_type": "long"}},
        '-_score',
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


def fuzzy_match(query):
    fuzzy_fields = [
        "meetboutnummer",
        "bouwbloknummer",
        "locatie",
    ]

    return Q("multi_match",
             query=query, fuzziness="auto",
             max_expansions=50,
             prefix_length=2, fields=fuzzy_fields)


def autocomplete_query(client, query):
    """
    provice autocomplete suggestions
    """

    match_fields = [
        "meetboutnummer",
        "bouwbloknummer",
        "locatie",
    ]

    completions = [
        "meetboutnummer",
        "bouwbloknummer",
        "locatie",
    ]

    return (
        Search(client)
        .index(MEETBOUTEN)
        .query(
            Q(
                "multi_match",
                query=query, type="phrase_prefix", fields=match_fields)
            | fuzzy_match(query))
        .highlight(*completions, pre_tags=[''], post_tags=[''])
    )


class SearchTestViewSet(searchviews.SearchViewSet):
    url_name = 'search/test-list'
    search_query = search_meetbout_query


class SearchMeetboutViewSet(searchviews.SearchViewSet):
    """
    Given a query parameter `q`, this function returns a subset of
    all adressable objects that match the adres elastic search query.
    """
    url_name = 'search/meetbouten'
    search_query = search_meetbout_query

    def get_url(self, request, hit):
        return _get_url(request, hit)


def get_autocomplete_response(client, query):
    result = autocomplete_query(client, query)[0:20].execute()
    matches = OrderedDict()

    # group_by doc_type
    for r in result:
        doc_type = r.meta.doc_type.replace('_', ' ')

        if doc_type not in matches:
            matches[doc_type] = OrderedDict()

        h = r.meta.highlight
        for key in h:
            highlights = h[key]
            for match in highlights:
                matches[doc_type][match] = 1

    for doc_type in matches.keys():
        matches[doc_type] = [
            dict(item=m) for m in matches[doc_type].keys()][:5]

    return matches


class TypeaheadViewSet(searchviews.TypeaheadViewSet):
    """
    Autocomplete boutnummers
    """
    def get_autocomplete_response(self, client, query):
        return get_autocomplete_response(client, query)
