import factory
from factory import fuzzy

from .. import models


class PeilmerkFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Peilmerk

    id = fuzzy.FuzzyText(length=10)
    hoogte = fuzzy.FuzzyText(length=8)
    jaar = fuzzy.FuzzyDecimal(1)
    merk = fuzzy.FuzzyChoice(choices=(models.Peilmerk.MERK_CHOICES,))
    omschrijving = fuzzy.FuzzyText(length=30)
    windrichting = fuzzy.FuzzyText(length=1)
    muurvlak_x = fuzzy.FuzzyInteger(1)
    muurvlak_y = fuzzy.FuzzyInteger(1)
    rws_nummer = fuzzy.FuzzyText(length=10)
