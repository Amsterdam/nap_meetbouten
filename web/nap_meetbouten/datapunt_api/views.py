import logging
from collections import OrderedDict

from django.conf import settings

from elasticsearch_dsl import Search, Q

from datapunt_generic.generic import rest
from datapunt_generic.generic import searchviews

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
        slop=12,  # match "stephan preeker" with "stephan jacob preeker"
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
        Search()
            .using(client)
            .index(MEETBOUTEN)
            .query(
            mulitimatch_meetbout_Q(query)
        ).sort(*add_sorting())
    )


def match_Q(query):
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

    completions = [
        "meetboutnummer",
        "bouwbloknummer",
        "locatie",
    ]

    return (
        Search()
            .using(client)
            .index(MEETBOUTEN)
            .query(match_Q(query))
            .highlight(*completions, pre_tags=[''], post_tags=[''])
    )


def old_autocomplete_query(client, query: int):
    """
    replicated the current behavior in atlas where we only autocompleet meetboutnummers and not on underlying data.
    :return: Ordered set of responses (on meetboutnummer) closest to the requested query
    """
    return (
        Search()
        .using(client)
        .index(MEETBOUTEN)
        .query({
            "prefix": {
                "_display": query,
            }
        })
        .sort('_display')
    )


class SearchTestViewSet(searchviews.SearchViewSet):
    url_name = 'search/test-list'
    search_query = search_meetbout_query


class SearchMeetboutViewSet(searchviews.SearchViewSet):
    """
    Zoek-Meetbouten

    Given a query parameter `q`, this function returns a subset of
    all adressable objects that match the adres elastic search query.

    """

    url_name = 'search/meetbouten'
    search_query = search_meetbout_query

    def get_url(self, request, hit):
        return _get_url(request, hit)

    def list(self, request, *args, **kwargs):
        """
        Show search results

        ---
        parameters:
            - name: q
              description: Zoek op meetboutnummertje
              required: true
              type: string
              paramType: query
        """

        return super(SearchMeetboutViewSet, self).list(
            request, *args, **kwargs)


def get_autocomplete_response(client, query):

    result = old_autocomplete_query(client, query)[0:10].execute()

    content = [{
            '_display': '{v}'.format(v=hit['_display']),
            'uri': 'meetbouten/meetbout/{v}'.format(v=hit['meetboutnummer'])
        } for hit in result.hits]

    return [{
        'label': 'Meetbouten',
        'content': content
    }]


class TypeaheadViewSet(searchviews.TypeaheadViewSet):
    """
    Autocomplete boutnummers
    """

    def get_autocomplete_response(self, client, query):
        return get_autocomplete_response(client, query)

    def list(self, request, *args, **kwargs):
        """
        Show search results

        ---
        parameters_strategy: merge

        parameters:
            - name: q
              description: Autcomplete op meetboutnummertje
              required: true
              type: string
              paramType: query
        """

        return super(TypeaheadViewSet, self).list(
            request, *args, **kwargs)
