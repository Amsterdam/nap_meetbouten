import logging
from collections import OrderedDict

from django.conf import settings

from rest_framework import viewsets, metadata
from rest_framework.response import Response
from rest_framework.reverse import reverse

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q
from elasticsearch.exceptions import TransportError

log = logging.getLogger('search')


class QueryMetadata(metadata.SimpleMetadata):
    def determine_metadata(self, request, view):
        result = super().determine_metadata(request, view)
        result['parameters'] = dict(
            q=dict(
                type="string",
                description="The query to search for",
                required=False
            )
        )
        return result


class TypeaheadViewSet(viewsets.ViewSet):
    """
    Given a query parameter `q`, this function returns a
    subset of all objects
    that (partially) match the specified query.

    *NOTE*

    We assume spelling errors and therefore it is possible
    to have unexpected results

    """

    def get_autocomplete_response(self, client, query):
        raise NotImplementedError

    metadata_class = QueryMetadata

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.client = Elasticsearch(settings.ELASTIC_SEARCH_HOSTS)

    def list(self, request, *args, **kwargs):
        if 'q' not in request.query_params:
            return Response([])

        query = request.query_params['q'].strip()

        if len(query) < 5 or not query.isdigit():
            return Response([])

        response = self.get_autocomplete_response(self.client, int(query))
        return Response(response)


def mulitimatch_Q(query):
    """
    main 'One size fits all' search query used
    """
    log.debug('%20s %s', mulitimatch_Q.__name__, query)

    return Q(
        "multi_match",
        query=query,
        type="phrase_prefix",
        slop=12,
        max_expansions=12,
        fields=[
            'naam',
            'straatnaam',
            'aanduiding',
            'adres',

            'postcode',
            'huisnummer'
            'huisnummer_variation',
        ]
    )


def default_search_query(client, query: str):
    """
    Execute search.

    ./manage.py test datapunt_api.tests.test_query --keepdb

    """

    return (
        Search()
        .using(client)
        .query(
            mulitimatch_Q(query)
        )
    )


def _get_url(_request, _hit):
    """
    return url to your api endpoints
    """
    None


class SearchViewSet(viewsets.ViewSet):
    """
    Given a query parameter `q`, this function returns a subset of all objects
    that match the elastic search query.

    *NOTE*

    We assume the input is correct but could be incomplete

    for example: seaching for a not existing
    Rozengracht 3 will rerurn Rozengracht 3-1 which does exist
    """

    metadata_class = QueryMetadata
    search_query = default_search_query
    page_size = 100
    url_name = 'search-list'

    def _set_followup_url(self, request, result, end,
                          response, query, page):
        """
        Add pageing links for result set to response object
        """

        followup_url = "{}?q={}".format(
            reverse(self.url_name, request=request),
            query)
        if 'page_size' in request.query_params:
            followup_url = "{}&page_size={}".format(
                followup_url,
                int(request.query_params['page_size']))

        prev_page = None
        if page == 1:
            pass
        elif page == 2:
            prev_page = followup_url
        else:
            prev_page = "{}&page={}".format(followup_url, page - 1)

        total = result.hits.total

        if end >= total:
            next_page = None
        else:
            next_page = "{}&page={}".format(followup_url, page + 1)

        self_url = followup_url
        if page != 1:
            self_url = "{}&page={}".format(self_url, page)

        response['_links'] = OrderedDict([
            ('self', dict(href=self_url)),
        ])

        if next_page:
            response['_links']['next'] = dict(href=next_page)
        else:
            response['_links']['next'] = None

        if prev_page:
            response['_links']['previous'] = dict(href=prev_page)
        else:
            response['_links']['previous'] = None
        return response

    def list(self, request, *args, **kwargs):

        if 'q' not in request.query_params:
            return Response([])

        page = 1
        if 'page' in request.query_params:
            page = int(request.query_params['page'])

        page_size = self.page_size
        if 'page_size' in request.query_params:
            page_size = int(request.query_params['page_size'])

        start = ((page - 1) * page_size)
        end = (page * page_size)

        query = request.query_params['q']
        query = query.lower()

        client = Elasticsearch(
            settings.ELASTIC_SEARCH_HOSTS,
            raise_on_error=True
        )

        search = self.search_query(client, query)[start:end]

        try:
            result = search.execute()
        except TransportError:
            log.exception("Could not execute search query " + query)
            # Todo fix this
            # https://github.com/elastic/elasticsearch/issues/11340#issuecomment-105433439
            return Response([])

        response = OrderedDict()

        response = self._set_followup_url(
            request=request,
            result=result,
            end=end,
            response=response,
            query=query,
            page=page)

        response['count'] = result.hits.total

        self.create_summary_aggregations(request, result, response)

        response['results'] = [
            self.normalize_hit(h, request) for h in result.hits]

        return Response(response)

    def create_summary_aggregations(self, request, result, response):
        """
        If there are aggregations within the search result.
        show them
        """
        # do noting yet

        return

        response['summary'] = []

        response['summary'] = [
            self.normalize_bucket(field, request)
            for field in result.aggregations['by_subtype']['buckets']]

        response['summary2'] = [
            self.normalize_bucket(field, request)
            for field in result.aggregations['by_type']['buckets']]

    def get_url(self, request, hit):
        """
        Get a detail API url for hit
        """
        return _get_url()

    def normalize_hit(self, hit, request):
        result = OrderedDict()
        result['_links'] = self.get_url(request, hit)

        result['type'] = hit.meta.doc_type
        result['dataset'] = hit.meta.index

        result.update(hit.to_dict())

        return result

    def normalize_bucket(self, field, request):
        # print(field)
        result = OrderedDict()
        result.update(field.to_dict())
        return result
