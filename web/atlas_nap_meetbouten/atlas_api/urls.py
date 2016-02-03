from django.conf.urls import url, include
from rest_framework import routers

from django.conf import settings

from datasets.nap.views import PeilViewSet
from datasets.meetbouten.views import *

from . import views as searchviews


class DocumentedRouter(routers.DefaultRouter):
    """
    NAP
    Het Normaal Amsterdams Peil (meestal afgekort tot NAP) is de referentiehoogte waaraan hoogtemetingen in Nederland
    worden gerelateerd. Het NAP-net bestaat uit ongeveer 50.000 zichtbare peilmerken en 250 ondergrondse peilmerken in
    Nederland, waarvan ongeveer 1000 in Amsterdam.

    Meetbouten
    In Amsterdam is een systeem gerealiseerd voor het monitoren van deformatie (zakkingen). De oudere, vooroorlogse
    panden in Amsterdam zijn gebouwd op houten palen. De kwaliteit van deze fundering op houten palen verschilt sterk.
    Een slechte fundering kan zakkingen tot gevolg hebben, waardoor de kwaliteit van deze panden afneemt en
    mogelijkerwijs zelfs uiteindelijk tot sloop kan leiden.

    Om dergelijke zakkingen te kunnen volgen zijn op grote schaal meetbouten geplaatst in de binnenstad, de 19e eeuwse
    gordel en de gordel 20-40, grofweg alle gebieden binnen de ringweg. Met de meetgegevens wordt vooral het inzicht
    vergroot in grootte en snelheid van de zakking. Eigenaren van de panden kunnen met deze inzichten rekening houden
    bij mogelijke investeringen. De Registratie meetbouten is een initiatief van de afdeling Wonen (opdrachtgever), de
    bestuurscommissies en de afdeling Basisinformatie.
    """

    def get_api_root_view(self):
        view = super().get_api_root_view()
        cls = view.cls

        class Datapunt(cls):
            pass

        Datapunt.__doc__ = self.__doc__
        return Datapunt.as_view()


router = DocumentedRouter()

router.register(r'nap/peilmerk', PeilViewSet)

router.register(r'meetbouten/meetbout', MeetboutViewSet)
router.register(r'meetbouten/meting', MetingViewSet)
router.register(r'meetbouten/referentiepunt', ReferentiepuntViewSet)
router.register(r'meetbouten/rollaag', RollaagViewSet)


# Search related

router.register(r'meetbouten/typeahead',
                searchviews.TypeaheadViewSet, base_name='typeahead')

router.register(r'meetbouten/search',
                searchviews.SearchMeetboutViewSet, base_name='search')


if settings.DEBUG:
    router.register(r'meetbouten/search/test',
                    searchviews.SearchTestViewSet,
                    base_name='search/test')


urlpatterns = [
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^', include(router.urls)),
]
