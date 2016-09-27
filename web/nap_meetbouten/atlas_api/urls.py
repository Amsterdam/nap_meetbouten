from rest_framework import routers

from datasets.meetbouten.views import *
from datasets.nap.views import PeilViewSet
from . import views as searchviews


class NAPRouter(routers.DefaultRouter):
    """
    Het Normaal Amsterdams Peil (meestal afgekort tot NAP) is de referentiehoogte waaraan hoogtemetingen in Nederland
    worden gerelateerd. Het NAP-net bestaat uit ongeveer 50.000 zichtbare peilmerken en 250 ondergrondse peilmerken in
    Nederland, waarvan ongeveer 1000 in Amsterdam.
    """

    def get_api_root_view(self, **kwargs):
        view = super().get_api_root_view(**kwargs)
        cls = view.cls

        class NAP(cls):
            pass

        NAP.__doc__ = self.__doc__
        return NAP.as_view()


class MeetboutenRouter(routers.DefaultRouter):
    """
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

    def get_api_root_view(self, **kwargs):
        view = super().get_api_root_view(**kwargs)
        cls = view.cls

        class Meetbouten(cls):
            pass

        Meetbouten.__doc__ = self.__doc__
        return Meetbouten.as_view()


meetbouten = MeetboutenRouter()

meetbouten.register(r'meetbout', MeetboutViewSet)
meetbouten.register(r'meting', MetingViewSet)
meetbouten.register(r'referentiepunt', ReferentiepuntViewSet)
meetbouten.register(r'rollaag', RollaagViewSet)

meetbouten.register(r'typeahead', searchviews.TypeaheadViewSet, base_name='typeahead')
meetbouten.register(r'search', searchviews.SearchMeetboutViewSet, base_name='search')

nap = NAPRouter()
nap.register(r'peilmerk', PeilViewSet)
