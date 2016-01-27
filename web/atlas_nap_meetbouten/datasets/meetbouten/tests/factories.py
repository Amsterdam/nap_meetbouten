import factory
from factory import fuzzy

from .. import models
from datasets.nap.tests.factories import PeilmerkFactory


class MeetboutFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Meetbout

    id = fuzzy.FuzzyText(length=10)
    bouwblokzijde = fuzzy.FuzzyText(length=10)
    status = fuzzy.FuzzyChoice(choices=(
        models.Meetbout.STATUS_VERVALLEN,
        models.Meetbout.STATUS_ACTUEEL)
    )


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
