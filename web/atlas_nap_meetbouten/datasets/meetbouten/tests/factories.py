import factory
from factory import fuzzy

from .. import models
from datasets.nap.tests.factories import PeilmerkFactory


class MeetboutFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Meetbout

    id = fuzzy.FuzzyText(length=10)
    locatie_x = fuzzy.FuzzyInteger(low=1, high=10)
    locatie_y = fuzzy.FuzzyInteger(low=1, high=10)
    locatie = fuzzy.FuzzyText()
    bouwblokzijde = fuzzy.FuzzyText(length=10)
    blokeenheid = fuzzy.FuzzyText(length=10)
    status = fuzzy.FuzzyChoice(choices=(
        models.Meetbout.STATUS_VERVALLEN,
        models.Meetbout.STATUS_ACTUEEL)
    )
    eigenaar = fuzzy.FuzzyText(length=50)
    nabij_adres = fuzzy.FuzzyText(length=30)
    bouwbloknummer = fuzzy.FuzzyText(length=4)
    stadsdeel_code = fuzzy.FuzzyText(length=3)


class ReferentiepuntFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Referentiepunt

    locatie = fuzzy.FuzzyText(length=10)
    peilmerk = factory.SubFactory(PeilmerkFactory)


class MetingFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Meting

    id = fuzzy.FuzzyText(length=10)
    type = fuzzy.FuzzyChoice(choices=(
        models.Meting.TYPE_NULMETING,
        models.Meting.TYPE_SCHATTING)
    )
    meetbout = factory.SubFactory(MeetboutFactory)
    refereert_aan = factory.SubFactory(ReferentiepuntFactory)


class RollaagFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Referentiepunt

    id = fuzzy.FuzzyInteger(low=1, high=100)
    meetbout = factory.SubFactory(MeetboutFactory)
