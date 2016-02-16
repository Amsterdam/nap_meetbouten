from django.conf.urls import url, include
from django.contrib import admin
# from django.views import generic
import atlas_api.urls
import datapunt_generic.batch.views as b_views

urlpatterns = [
    url(r'^jobs/?$', b_views.JobListView.as_view(), name='job-list'),
    url(r'^jobs/(?P<pk>.*)$', b_views.JobDetailView.as_view(), name='job-detail'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^status/', include('datapunt_generic.health.urls', namespace='health')),

    url(r'^nap/', include(atlas_api.urls.nap.urls)),
    url(r'^meetbouten/', include(atlas_api.urls.meetbouten.urls)),
]
