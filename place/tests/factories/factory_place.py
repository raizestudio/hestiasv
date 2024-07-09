import factory
from faker import Faker

fake = Faker()


class PlaceFactory(factory.django.DjangoModelFactory):
    """Place factory"""

    class Meta:
        model = "place.Place"

    name = factory.LazyAttribute(lambda _: fake.word())
    description = factory.LazyAttribute(lambda _: fake.text())
