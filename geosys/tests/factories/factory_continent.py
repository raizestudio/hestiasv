import factory
from faker import Faker

fake = Faker()


class ContinentFactory(factory.django.DjangoModelFactory):
    """Continent factory"""

    class Meta:
        model = "geosys.Continent"

    code = factory.LazyAttribute(lambda _: fake.random_letters(length=2))
    name = factory.LazyAttribute(lambda _: fake.name())
    slug = factory.LazyAttribute(lambda _: fake.slug())
