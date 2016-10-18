from django.conf.urls import url, include
# from django.contrib import admin
# from django.views import generic
import atlas_api.urls

import coreapi
from coreapi import Link, Field

from rest_framework import renderers, schemas, response

from rest_framework.decorators import api_view, renderer_classes

from rest_framework_swagger.renderers import OpenAPIRenderer
from rest_framework_swagger.renderers import SwaggerUIRenderer


api_schema = coreapi.Document(
    title='test coreapi',
    content={
        'docs': {'read': Link(url='/nap/docs/', action='get')},

        'meetbout': {
            'list': Link(
                url='/meetbouten/meetbout/', action='get',
                fields=[
                        Field('page', location='query'),
                        Field('page_size', location='query'),
                        Field('bouwbloknummer', location='query'),
                        Field('rollaag', location='query')
                ]),
            'retrieve': Link(
                url='/meetbouten/meetbout/{pk}/', action='get',
                fields=[
                    Field('pk', required=True, location='path')
                ])
            },
        'meetbouten': {'read': Link(url='/meetbouten/', action='get')},
        'meting': {
            'list': Link(
                url='/meetbouten/meting/',
                action='get',
                fields=[
                    Field('page', location='query'),
                    Field('page_size', location='query'),
                    Field('meetbout', location='query'),
                    Field('refereert_aan__id', location='query')]),
            'retrieve': Link(
                url='/meetbouten/meting/{pk}/',
                action='get',
                fields=[
                    Field('pk', required=True, location='path')]
            )},

        'nap': {'read': Link(url='/nap/', action='get')},

        'peilmerk': {
            'list': Link(
                url='/nap/peilmerk/', action='get',
                description='test',
                fields=[
                    Field('page', location='query'),
                    Field('page_size', location='query'),
                    Field('omschrijving', location='query')]),

            'retrieve': Link(
                url='/nap/peilmerk/{pk}/',
                action='get', fields=[
                    Field('pk', required=True, location='path')]
                )},

        'referentiepunt': {

            'list': Link(
                url='/meetbouten/referentiepunt/',
                action='get',
                fields=[
                    Field('page', location='query'),
                    Field('page_size', location='query'),
                    Field('metingen__id', location='query')
                ]),

            'retrieve': Link(
                url='/meetbouten/referentiepunt/{pk}/',
                action='get',
                fields=[
                    Field('pk', required=True, location='path')]
                )},

            'rollaag': {
                'list': Link(
                    url='/meetbouten/rollaag/',
                    action='get',
                    fields=[
                        Field('page', location='query'),
                        Field('page_size', location='query')]),
                'retrieve': Link(
                        url='/meetbouten/rollaag/{pk}/',
                        action='get',
                        fields=[
                            Field('pk', required=True, location='path')]
                        )
                },

            'search': {
                'list': Link(
                    url='/meetbouten/search/',
                    action='get')},

            'typeahead': {
                'list':
                Link(url='/meetbouten/typeahead/', action='get')}
        })


@api_view()
@renderer_classes([
    SwaggerUIRenderer, OpenAPIRenderer, renderers.CoreJSONRenderer])
def schema_view(request):
    generator = schemas.SchemaGenerator(title='NAP Meetbouten API')
    # crash
    # here we need to add custom schema!
    return response.Response(generator.get_schema(request=request))


@api_view()
@renderer_classes([
    SwaggerUIRenderer, OpenAPIRenderer, renderers.CoreJSONRenderer])
def schema_view_test(request):
    # here we need to add custom schema!
    return response.Response(api_schema)


urlpatterns = [

    url('^nap/docs/$', schema_view),
    url('^nap/docs_2/$', schema_view_test),
    url('^thedoc$', schema_view_test),

    url(r'^status/',
        include('datapunt_generic.health.urls', namespace='health')),

    url(r'^nap/', include(atlas_api.urls.nap.urls)),

    # url(r'^meetbouten/docs/', include('rest_framework_swagger.urls')),

    url(r'^meetbouten/', include(atlas_api.urls.meetbouten.urls)),
]
