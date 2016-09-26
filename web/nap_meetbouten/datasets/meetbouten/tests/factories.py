import factory
from factory import fuzzy

from .. import models


class RollaagFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Rollaag

    id = fuzzy.FuzzyInteger(low=1, high=100)
    bouwblok = fuzzy.FuzzyText(length=4)


class MeetboutFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Meetbout

    id = fuzzy.FuzzyText(length=10)

    bouwbloknummer = fuzzy.FuzzyText(length=4)

    bouwblokzijde = fuzzy.FuzzyText(length=10)
    status = fuzzy.FuzzyChoice(choices=(
        models.Meetbout.STATUS_VERVALLEN,
        models.Meetbout.STATUS_ACTUEEL)
    )
    rollaag = factory.SubFactory(RollaagFactory)


class ReferentiepuntFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Referentiepunt

    id = fuzzy.FuzzyText(length=10)
    locatie = fuzzy.FuzzyText(length=10)


class MetingFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Meting

    id = fuzzy.FuzzyText(length=10)
    type = fuzzy.FuzzyChoice(choices=(
        models.Meting.TYPE_NULMETING,
        models.Meting.TYPE_SCHATTING)
    )
    meetbout = factory.SubFactory(MeetboutFactory)
