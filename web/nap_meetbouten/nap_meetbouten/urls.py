from django.conf.urls import url, include
from django.conf import settings
from rest_framework import schemas, response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import CoreJSONRenderer
from rest_framework_swagger.renderers import OpenAPIRenderer
from rest_framework_swagger.renderers import SwaggerUIRenderer

import atlas_api.urls

grouped_url_patterns = {
    'base_patterns': [
        url(r'^status/',
            include('datapunt_generic.health.urls', namespace='health')),
    ],
    'nap_patterns': [
        url(r'^nap/', include(atlas_api.urls.nap.urls)),
    ],
    'meetbouten_patterns': [
        url(r'^meetbouten/', include(atlas_api.urls.meetbouten.urls)),
    ],
}


@api_view()
@renderer_classes([SwaggerUIRenderer, OpenAPIRenderer, CoreJSONRenderer])
def meetbouten_schema_view(request):
    generator = schemas.SchemaGenerator(
        title='Registratie Meetbouten API',
        patterns=grouped_url_patterns['meetbouten_patterns']
    )
    return response.Response(generator.get_schema(request=request))


@api_view()
@renderer_classes([SwaggerUIRenderer, OpenAPIRenderer, CoreJSONRenderer])
def peilmerken_schema_view(request):
    generator = schemas.SchemaGenerator(
        title='NAP Peilmerken API',
        patterns=grouped_url_patterns['nap_patterns']
    )
    return response.Response(generator.get_schema(request=request))


urlpatterns = [
    url('^meetbouten/docs/api-docs/meetbouten/$', meetbouten_schema_view),
    url('^meetbouten/docs/api-docs/nap/$', peilmerken_schema_view),

    ] + [url for pattern_list in grouped_url_patterns.values()
         for url in pattern_list]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns.append(url(r'^__debug__/', include(debug_toolbar.urls)))
