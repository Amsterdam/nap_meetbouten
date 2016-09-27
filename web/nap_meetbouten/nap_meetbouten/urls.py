from django.conf.urls import url, include
# from django.contrib import admin
# from django.views import generic
import atlas_api.urls

urlpatterns = [

    # url(r'^admin/', include(admin.site.urls)),

    url(r'^status/',
        include('datapunt_generic.health.urls', namespace='health')),

    url(r'^nap/', include(atlas_api.urls.nap.urls)),

    # url(r'^meetbouten/docs/', include('rest_framework_swagger.urls')),

    url(r'^meetbouten/', include(atlas_api.urls.meetbouten.urls)),
]
