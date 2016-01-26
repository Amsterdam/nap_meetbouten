import factory
from factory import fuzzy

from .. import models


class PeilmerkFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Peilmerk

    id = fuzzy.FuzzyText(length=10)
    jaar = fuzzy.FuzzyDecimal(low=1985, high=2016)
    merk = fuzzy.FuzzyChoice(choices=(
        models.Peilmerk.MERK_0,
        models.Peilmerk.MERK_1)
    )
    omschrijving = fuzzy.FuzzyText(length=30)
    windrichting = fuzzy.FuzzyText(length=1)
    muurvlak_x = fuzzy.FuzzyInteger(low=1, high=10)
    muurvlak_y = fuzzy.FuzzyInteger(low=1, high=10)
    rws_nummer = fuzzy.FuzzyText(length=10)
